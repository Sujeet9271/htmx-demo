from django.contrib import admin
from accounts.models import Users, Project, Menu, SubMenu, Tickets, Event
# Register your models here.


admin.site.register(Users)
admin.site.register(Project)
admin.site.register(Menu)
admin.site.register(SubMenu)
admin.site.register(Tickets)
admin.site.register(Event)