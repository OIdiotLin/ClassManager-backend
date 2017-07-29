from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from classmanager.sensitive import PASSWORD_CLIENT

# Use Token
from app.utils.token import token_check

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt

from hashlib import md5


@csrf_exempt
def login(request):
	"""
	login
	:param request:
	:return: check code (md5)
	"""
	if request.method == 'POST' and token_check(request):
		if request.POST['password'] == PASSWORD_CLIENT:

			return JsonResponse({
				'check_code': md5().update(request.body.decode('utf-8').encode('utf-8')).hexdigest()
			})

