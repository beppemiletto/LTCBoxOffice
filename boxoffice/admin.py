from django.contrib import admin
from .models import SellingSeats

class SellingSeatsAdmin(admin.ModelAdmin):
    list_display = ('event', 'seat') 

# Register your models here.
admin.site.register(SellingSeats, SellingSeatsAdmin)

