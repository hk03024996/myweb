from django.contrib import admin
from .models import LiveType, Live

# Register your models here.
@admin.register(LiveType)
class LiveTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")

@admin.register(Live)
class LiveAdmin(admin.ModelAdmin):
    list_display = ("title", "live_type", "author", "readed_num", "click_nums", "image")


