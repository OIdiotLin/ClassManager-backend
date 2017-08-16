from django.conf.urls import url
from django.contrib import admin

from app.views.person import *
from app.views.activity import *
from app.views.qiniuhelper import *
from app.views.account import *
from app.views.feedback import *
from app.views.finance import *

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

	# FEEDBACK
	url(r'api/add_feedback/', add_feedback),

	# FINANCE
	url(r'api/add_finance/', add_finance),
	url(r'api/get_balance/', get_balance),
	url(r'api/get_finance_list/', get_finance_list),
	url(r'api/delete_finance/', delete_finance),
	url(r'api/update_finance/', update_finance)
]
