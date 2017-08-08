from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from classmanager.sensitive import *

# Use Token
from app.utils.token import token_check

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt

from hashlib import md5

import json


@csrf_exempt
def login(request):
	"""
	login
	:param request:
	:return: check code (md5)
	"""
	if request.method == 'POST':
		pswd = json.loads(request.body.decode('utf-8'))['password']
		if pswd == PASSWORD_CLIENT:
			encoder = md5()
			encoder.update(request.body.decode('utf-8').encode('utf-8'))
			return JsonResponse({
				'check_code': EXT_STRING
			})

