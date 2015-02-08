from django.contrib import admin
from reserve.models import staff

# Register your models here.


class staffAdmin(admin.ModelAdmin):
    list_display=('name','stuid','phone','email')

admin.site.register(staff,staffAdmin)
