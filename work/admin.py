from asyncio import Task
from django.contrib import admin
from .models import *
from .forms import UserForm
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_complete']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id']


@admin.register(History)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'status']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'status', 'created_at']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(InviteLink)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'project']
