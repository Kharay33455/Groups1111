from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Address)
admin.site.register(Agent)
admin.site.register(Verification)
admin.site.register(Message)