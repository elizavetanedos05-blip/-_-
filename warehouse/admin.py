from django.contrib import admin
from .models import Worker, SpecOdejda, IssuedItem


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position')
    search_fields = ('full_name',)


@admin.register(SpecOdejda)
class SpecOdejdaAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'size', 'quantity_in_stock', 'norm_days')
    list_filter = ('type',)


@admin.register(IssuedItem)
class IssuedItemAdmin(admin.ModelAdmin):
    list_display = ('worker', 'spec_odejda', 'issue_date', 'wear_level', 'status')
    list_filter = ('status',)