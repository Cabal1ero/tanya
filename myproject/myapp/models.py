from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Краткая информация')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    def get_first_image(self):
        return self.images.first()

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/', verbose_name='Фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Фото услуги'
        verbose_name_plural = 'Фото услуг'
        ordering = ['order']
    
    def __str__(self):
        return f"Фото для услуги: {self.service.name}"


    
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    position = models.CharField(max_length=100, verbose_name='Должность')
    bio = models.TextField(verbose_name='Краткая информация')
    classification = models.CharField(max_length=50, verbose_name='Классификация', default='Не указано')
    image = models.ImageField(upload_to='team/', verbose_name='Фото', null=True, blank=True)
    services = models.ManyToManyField(Service, related_name='masters', verbose_name='Услуги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команды'



class Appointment(models.Model):
    client_name = models.CharField('Имя клиента', max_length=100, null=True)
    client_phone = models.CharField('Номер телефона', max_length=20, null=True)
    time_slot = models.OneToOneField('TimeSlot', on_delete=models.CASCADE, verbose_name='Временной слот', null=True)
    created_at = models.DateTimeField('Дата создания записи', auto_now_add=True)

    def __str__(self):
        return f'Запись для {self.client_name} на {self.time_slot.date} в {self.time_slot.start_time}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.name}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class PortfolioWork(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название работы')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='portfolio/', verbose_name='Фото работы')
    stylist = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, verbose_name='Мастер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пример работы'
        verbose_name_plural = 'Примеры работ'


class TimeSlot(models.Model):
    master = models.ForeignKey(TeamMember, on_delete=models.CASCADE, verbose_name='Мастер')
    date = models.DateField('Дата')
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField('Время окончания')
    is_available = models.BooleanField('Доступно', default=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name='Услуга')

    class Meta:
        verbose_name = 'Временное окно'
        verbose_name_plural = 'Временные окна'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.master} - {self.date} {self.start_time}"
    

class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Фоновое изображение', upload_to='hero_slides/')
    button_text = models.CharField('Текст кнопки', max_length=50, default='Подробнее')
    button_link = models.CharField('Ссылка для кнопки', max_length=200, default='#services')
    is_visible = models.BooleanField('Показывать на сайте', default=True)
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Слайды с меньшим номером отображаются первыми')

    class Meta:
        verbose_name = 'Слайд на главной'
        verbose_name_plural = 'Слайды на главной'
        ordering = ['order']

    def __str__(self):
        return self.title

    
