from django.contrib import admin
from .models import Service, TeamMember, Review, Appointment, TimeSlot,PortfolioWork, ServiceImage, HeroSlide


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price'] 
    inlines = [ServiceImageInline]
    
    def __str__(self):
        return self.name

admin.site.register(Service, ServiceAdmin)

admin.site.register(TeamMember)
admin.site.register(Review)
admin.site.register(TimeSlot)
admin.site.register(PortfolioWork)

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_visible')
    list_editable = ('order', 'is_visible')
    list_display_links = ('title',)

# Register your models here.
