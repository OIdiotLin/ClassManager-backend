from django.conf.urls import url
from django.contrib import admin

from app.views.person import *
from app.views.activity import *
from app.views.qiniuhelper import *
from app.views.account import *

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	# PERSON
	url(r'^api/get_person_list/', get_person_list),
	url(r'^api/add_person/', add_person),
	url(r'^api/delete_person/', delete_person),
	url(r'^api/update_person/', update_person),
	url(r'^api/get_person_by_activity/', get_person_by_activity),

	# ACTIVITY
	url(r'^api/get_activity_list/', get_activity_list),
	url(r'^api/add_activity/', add_activity),
	url(r'^api/delete_activity/', delete_activity),
	url(r'^api/update_activity/', update_activity),

	# QINIU
	url(r'api/get_upload_token/', get_upload_token),

	# ACCOUNT
	url(r'api/login/', login),
]
