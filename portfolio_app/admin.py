from django.contrib import admin
from portfolio_app.models import *

class treeview(admin.ModelAdmin):
    list_display=['name','email','subject','message']
admin.site.register(visitorquery,treeview)

