from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.db import DatabaseError

# Use Token
from app.utils.token import token_check

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt

# Models
from app.models import Feedback

import json


@csrf_exempt
def add_feedback(request):
	"""
	Add new feedback into MySQL databases
	Http form MUST includes `summary`, `category`, `contact`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST':
		try:
			feedback_info = json.loads(request.body.decode('utf-8'))['feedback']

			new_feedback = Feedback(
				summary = feedback_info['summary'],
				category = feedback_info['category'],
				contact = feedback_info['contact'],
				details = feedback_info['details'] if 'details' in feedback_info.keys() else ''
			)

			new_feedback.save()
			return JsonResponse({'status': 'success'})

		except DatabaseError as e:
			return JsonResponse(
				{
					'status': 'fail',
					'err_code': e.args[0],
					'err_info': e.args[1],
				}
			)
