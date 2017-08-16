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


@csrf_exempt
def delete_finance(request):
	"""
	Delete finance
	:param request: httpRequest - POST
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST' and token_check(request):

		try:
			finance_info = json.loads(request.body.decode('utf-8'))['finance']

			target_finance = Finance.objects.filter(
				id = finance_info['id']
			)
			if not target_finance.exists():
				return JsonResponse({
						'status': 'fail',
						'err_code': 404,
						'err_info': 'no object has id = ' + finance_info['id']
				})
			
			target_finance.delete()
			return JsonResponse({'status': 'success'})

		except DatabaseError as e:
			return JsonResponse(
				{
					'status': 'fail',
					'err_code': e.args[0],
					'err_info': e.args[1],
				}
			)


@csrf_exempt
def update_finance(request):
	"""
	Update a finance operation in databases
	:param request: HttpRequest
	:return: status (success or fail), err_info and err_code
									doesn't exist	0
	"""
	if request.method == 'POST' and token_check(request):

		try:
			target_id = json.loads(request.body.decode('utf-8'))['id']
			finance_info = json.loads(request.body.decode('utf-8'))['finance']

			target_finance = Finance.objects.get(
				id = target_id
			)

			if not target_finance:
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 404,
						'err_info': 'no object has id = ' + id
					}
				)

			for key in finance_info:
				exec('target_finance.' + key + '=' + str(repr(finance_info[key])))
			target_finance.save()

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
