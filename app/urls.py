from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^doc/api/', views.show_api),
	url(r'^api/get_person_list/', views.get_person_list),
	url(r'^api/add_person/', views.add_person),
	url(r'^api/delete_person/', views.delete_person),
	url(r'^api/update_person/', views.update_person)
]
