from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, TeamMember, Review, TimeSlot, TeamMember, PortfolioWork, Appointment, HeroSlide
from .forms import  ReviewForm

from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


class ScheduleView(ListView):
    model = TimeSlot
    template_name = 'myapp/home.html'
    context_object_name = 'slots'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['dates'] = [today + timedelta(days=x) for x in range(7)]
        context['masters'] = TeamMember.objects.all()
        context['schedule'] = self.get_schedule_data(context['dates'], context['masters'])
        context['team_members'] = TeamMember.objects.all()
        context['available_slots'] = self.get_available_slots(context['dates'], context['masters'])
        return context

    @classmethod
    def get_schedule_data(cls, dates, masters):
        schedule = {}
        start_date = dates[0]
        end_date = dates[-1]
        for master in masters:
            slots = TimeSlot.objects.filter(
                master=master,
                date__range=[start_date, end_date],
                is_available=True  
            ).order_by('date', 'start_time')
            
            if slots.exists():  # Проверяем, есть ли доступные слоты
                schedule[master] = {}
                for date in dates:
                    schedule[master][date] = [slot for slot in slots if slot.date == date]
        
        return schedule
    @classmethod
    def get_available_slots(cls, dates, masters):
        start_date = dates[0]
        end_date = dates[-1]
        available_slots = TimeSlot.objects.filter(
            master__in=masters,
            date__range=[start_date, end_date],
            is_available=True
        ).order_by('date', 'start_time')
        return available_slots

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def home(request):
    services = Service.objects.all()
    team_members = TeamMember.objects.all()
    reviews = Review.objects.order_by('-date')[:5]  # Последние 5 отзывов
    portfolio_works = PortfolioWork.objects.all()
    hero_slides = HeroSlide.objects.filter(is_visible=True)
    review_form = ReviewForm()
    
    context = {
        'services': services,
        'team_members': team_members,
        'reviews': reviews,
        'portfolio_works': portfolio_works,
        'review_form': review_form,
        'hero_slides': hero_slides,
    }
    return render(request, 'home.html', context)


def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})

# API Views
def get_masters_for_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    masters = service.masters.all()
    masters_data = [{'id': master.id, 'name': master.name} for master in masters]
    return JsonResponse(masters_data, safe=False)

def get_time_slots(request, master_id, date):
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    slots = TimeSlot.objects.filter(
        master_id=master_id, 
        is_available=True, 
        date=selected_date
    ).order_by('start_time')
    
    slots_by_period = {
        'morning': [],
        'day': [],
        'evening': []
    }
    
    for slot in slots:
        slot_data = {'id': slot.id, 'time': slot.start_time.strftime('%H:%M')}
        if 5 <= slot.start_time.hour < 12:
            slots_by_period['morning'].append(slot_data)
        elif 12 <= slot.start_time.hour < 18:
            slots_by_period['day'].append(slot_data)
        else:
            slots_by_period['evening'].append(slot_data)
            
    return JsonResponse(slots_by_period)

from django.db import transaction

@require_POST
def book_appointment(request):
    try:
        data = json.loads(request.body)
        timeslot_id = data.get('timeslot_id')
        client_name = data.get('client_name')
        client_phone = data.get('client_phone')
                
        if not all([timeslot_id, client_name, client_phone]):
            return JsonResponse({'status': 'error', 'message': 'Пожалуйста, заполните все поля.'}, status=400)
        
        # Используем транзакцию с блокировкой для избежания race condition
        with transaction.atomic():
            slot = TimeSlot.objects.select_for_update().get(pk=timeslot_id)
            
            if not slot.is_available:
                return JsonResponse({'status': 'error', 'message': 'Данное время уже занято.'}, status=400)
            
            # Создаем запись
            Appointment.objects.create(
                client_name=client_name,
                client_phone=client_phone,
                time_slot=slot
            )
                    
            # Помечаем слот как занятый
            slot.is_available = False
            slot.save()
            
        return JsonResponse({'status': 'success', 'message': 'Вы успешно записаны!'})
        
    except TimeSlot.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Выбранное время не найдено.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Неверный формат данных.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    try:
        data = json.loads(request.body)
        timeslot_id = data.get('timeslot_id')
        client_name = data.get('client_name')
        client_phone = data.get('client_phone')
        
        if not all([timeslot_id, client_name, client_phone]):
            return JsonResponse({'status': 'error', 'message': 'Пожалуйста, заполните все поля.'}, status=400)

        slot = get_object_or_404(TimeSlot, pk=timeslot_id)

        if not slot.is_available:
            return JsonResponse({'status': 'error', 'message': 'Данное время уже занято.'}, status=400)

        # Создаем запись
        Appointment.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            time_slot=slot
        )
        
        # Помечаем слот как занятый
        slot.is_available = False
        slot.save()

        return JsonResponse({'status': 'success', 'message': 'Вы успешно записаны!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Неверный формат данных.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)