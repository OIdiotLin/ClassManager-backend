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
from app.models import Person
from app.models import Activity

import json


def get_person_list(request):
	"""
	Get person list in MySQL databases
	:param request: httpRequest
	:return: person list(json)
	"""
	if request.method == 'GET':

		data = Person.objects.all()

		if 'name' in request.GET.keys():
			data = data.filter(name = request.GET['name'])

		if 'gender' in request.GET.keys():
			data = data.filter(gender = request.GET['gender'])

		if 'native_province' in request.GET.keys():
			data = data.filter(native_province = request.GET['native_province'])

		if 'dormitory' in request.GET.keys():
			data = data.filter(dormitory = request.GET['dormitory'])

		if 'birthday' in request.GET.keys():
			data = data.filter(birthday = request.GET['birthday'])

		if 'participation' in request.GET.keys():
			data = data.filter(participation = request.GET['participation'])

		if 'student_number' in request.GET.keys():
			data = data.filter(student_number = request.GET['student_number'])

		content = [dict(x) for x in data.values()]

		return JsonResponse({
			'count': data.count(),
			'result': content
		})


@csrf_exempt
def add_person(request):
	"""
	Add new person into MySQL databases
	Http form MUST includes `student_number`, `name`, `pinyin` and `gender`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST' and token_check(request):
		try:
			person_info = json.loads(request.body.decode('utf-8'))['person']

			new_person = Person(
				student_number = person_info['student_number'],
				name = person_info['name'],
				pinyin = person_info['pinyin'],
				gender = person_info['gender'],
				native_province = person_info['native_province'] if 'native_province' in person_info.keys() else '',
				dormitory = person_info['dormitory'] if 'dormitory' in person_info.keys() else '',
				birthday = person_info['birthday'] if 'birthday' in person_info.keys() else '2000-01-01',
				phone_number = person_info['phone_number'] if 'phone_number' in person_info.keys() else '',
				position = person_info['position'] if 'position' in person_info.keys() else '',
				participation = person_info['participation'] if 'participation' in person_info.keys() else 0
			)

			new_person.save()
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
def delete_person(request):
	"""
	Delete a person by his or her student_number
	Http form MUST includes `student_number`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
									doesn't exist	0
	"""
	if request.method == 'POST' and token_check(request):

		try:
			person_info = json.loads(request.body.decode('utf-8'))['person']

			target_person = Person.objects.filter(
				student_number = person_info['student_number']
			)
			if not target_person.exists():
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 404,
						'err_info': 'no object has student_number = ' + person_info['student_number']
					}
				)
			target_person.delete()
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
def update_person(request):
	"""
	Update a person in databases
	:param request: HttpRequest
	:return: status (success or fail), err_info and err_code
									doesn't exist	0
	"""
	if request.method == 'POST' and token_check(request):

		try:
			target_student_number = json.loads(request.body.decode('utf-8'))['target_student_number']
			person_info = json.loads(request.body.decode('utf-8'))['person']

			target_person = Person.objects.get(
				student_number = target_student_number
			)

			if not target_person:
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 404,
						'err_info': 'no object has student_number = ' + target_student_number
					}
				)

			for key in person_info:
				exec('target_person.' + key + '=' + str(repr(person_info[key])))
			target_person.save()

			return JsonResponse({'status': 'success'})

		except DatabaseError as e:
			return JsonResponse(
				{
					'status': 'fail',
					'err_code': e.args[0],
					'err_info': e.args[1],
				}
			)


def get_person_by_activity(request):
	"""
	get persons involved with activity
	:param request: Http request - get, args: id(activity_id)
	:return: Person.objects
	"""
	if request.method == 'GET':
		activity = Activity.objects.filter(pk = request.GET['id']).first()

		if not activity:
			return JsonResponse({
				'status': 'fail',
				'err_code': 404,
				'err_info': 'no activity has id = ' + request.GET['id']
			})

		data = Person.objects.none()
		for target in activity.participator.split(','):
			data = data | Person.objects.filter(student_number = target)

		content = [dict(x) for x in data.values()]

		return JsonResponse({
			'count': data.count(),
			'result': content
		})
