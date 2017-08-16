from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.db import DatabaseError
from django.db.models import Sum

# Use Token
from app.utils.token import token_check

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt

# Models
from app.models import Finance

import json


def get_finance_list(request):
	"""
	Get Finance list in databases
	:param request: httpRequest - GET
	:return: finance list (json)
	"""
	if request.method == 'GET':

		data = Finance.objects.all()
		content = [dict(f) for f in data.values()]

		return JsonResponse({
			'count': data.count(),
			'result': content
		})


@csrf_exempt
def add_finance(request):
	"""
	Add new financial operation into MySQL databases
	Http form MUST includes `income`, `expense`, `date` and `event`
	:param request: httpRequest - POST
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST' and token_check(request):
		try:
			finance_info = json.loads(request.body.decode('utf-8'))['finance']

			new_finance = Finance(
				event = finance_info['event'],
				date = finance_info['date'],
				income = finance_info['income'],
				expense = finance_info['expense'],
				details = finance_info['details'] if 'details' in finance_info.keys() else ''
			)

			new_finance.save()
			return JsonResponse({'status': 'success'})

		except DatabaseError as e:
			return JsonResponse(
				{
					'status': 'fail',
					'err_code': e.args[0],
					'err_info': e.args[1],
				}
			)


def get_balance(request):
	"""
	:param request: HttpRequest - GET
	:return: JsonResponse('balance')
	"""
	if request.method == 'GET':
		try:
			incomes = Finance.objects.all().aggregate(Sum('income'))['income__sum']
			expenses = Finance.objects.all().aggregate(Sum('expense'))['expense__sum']
			return JsonResponse({'balance': incomes-expenses})
		except :
			return JsonResponse(
				{
					'status': 'fail',
				}
			)
