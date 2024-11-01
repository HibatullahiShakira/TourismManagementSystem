from django.contrib import admin
from .models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'price', 'description']
    list_per_page = 10
    list_editable = ['price', 'name']
    search_fields = ['name']

    #@admin.display(ordering='inventory')
    #def inventory_status(self, tour: Tour):
        #if tour.inventory < 20:
            #return 'Low'
        #return 'Ok'
# Register your models here.
