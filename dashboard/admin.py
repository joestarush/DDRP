from django.contrib import admin
from .models import CustomUser, Index_page_info, Requirements, Feedback, Admin_additional_info, Temp_admin_save, temp_log_qr

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Index_page_info)
admin.site.register(Requirements)
admin.site.register(Feedback)
admin.site.register(Admin_additional_info)
admin.site.register(Temp_admin_save)
admin.site.register(temp_log_qr)



