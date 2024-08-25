from django.contrib import admin
from model.models import TICKET, USER, City, Stadium,matchlist
admin.site.register(City)
admin.site.register(Stadium)
admin.site.register(matchlist)
admin.site.register(TICKET)
admin.site.register(USER)

# Register your models here.
