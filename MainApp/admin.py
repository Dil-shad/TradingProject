from django.contrib import admin
from .models import Candle

# Register your models here.


class CandleAdmin(admin.ModelAdmin):
    list_display = ('open','high','low','close','date')

admin.site.register(Candle, CandleAdmin)
