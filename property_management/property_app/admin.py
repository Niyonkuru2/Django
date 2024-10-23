from django.contrib import admin

# Register your models here.
from .models import Property,Unit,Tenant,Lease
admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(Lease)
