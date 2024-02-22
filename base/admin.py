from django.contrib import admin
from .models import Address, Agent, Verification

# Register your models here.

admin.site.register(Address)
admin.site.register(Agent)
admin.site.register(Verification)