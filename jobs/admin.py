from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import User, Company, CV, Education, Job, Application, Experience

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(CV)
admin.site.register(Education)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Experience)