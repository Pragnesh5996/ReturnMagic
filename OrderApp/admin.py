from django.contrib import admin
from .models import about_data, Policy_data, detail_order, contact_details, Homedata
from django_dynamic_resource_admin.admin import DjangoDynamicResourceAdmin
from django.views.decorators.csrf import csrf_exempt
# Register your models here.


admin.site.register(about_data)
admin.site.register(Policy_data)
admin.site.register(Homedata)

class ContactAdmin(admin.ModelAdmin):
    list_display= ('shopname', 'fullname', 'email', 'subject_data', 'message_data')

    search_fields = ['fullname', 'shopname']
    
  
admin.site.register(contact_details, ContactAdmin)