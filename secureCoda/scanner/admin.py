from django.contrib import admin
from .models import Document, Table, Alert

# Register your models here.
admin.site.register(Document)
admin.site.register(Table)
admin.site.register(Alert)