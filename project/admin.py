from django.contrib import admin
from .models import MembershipType, Member, CheckIn, Payment
# Register your models here.

admin.site.register(MembershipType)
admin.site.register(Member)
admin.site.register(CheckIn)
admin.site.register(Payment)

