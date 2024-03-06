from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Address)
admin.site.register(Agent)
admin.site.register(Verification)
admin.site.register(Message)
admin.site.register(Prompt)
admin.site.register(BankAccount)
admin.site.register(BankName)