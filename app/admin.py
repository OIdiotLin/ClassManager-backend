from django.contrib import admin
from app.models import Person, Activity, Feedback, Finance

# Register your models here.


admin.site.register(Person)
admin.site.register(Activity)
admin.site.register(Feedback)
admin.site.register(Finance)
