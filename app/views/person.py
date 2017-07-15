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

		content = serializers.serialize('json', data)
		return HttpResponse(content, content_type = 'application/json')


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
			new_person = Person(
				student_number = request.POST.get('student_number'),
				name = request.POST.get('name'),
				pinyin = request.POST.get('pinyin'),
				gender = request.POST.get('gender'),
				native_province = request.POST.get('native_province', ''),
				dormitory = request.POST.get('dormitory', ''),
				birthday = request.POST.get('birthday', '2000-01-01'),
				phone_number = request.POST.get('phone_number', ''),
				position = request.POST.get('position', ''),
				participation = request.POST.get('participation', 0)
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
			target_person = Person.objects.filter(
				student_number = request.POST.get('student_number')
			)
			if not target_person.exists():
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 4004,
						'err_info': 'no object has student_number = ' + request.POST.get('student_number')
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
			target_person = Person.objects.get(
				student_number = request.POST.get('target_student_number')
			)
			if not target_person:
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 4004,
						'err_info': 'no object has student_number = ' + request.POST.get('target_student_number')
					}
				)
			# return JsonResponse(request.POST)

			for key in request.POST.keys():
				if not key == 'target_student_number':
					exec('target_person.' + key + '=' + str(repr(request.POST.get(key))))
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
		activity = obj = Activity.objects.filter(pk = request.GET['id']).first()

		if not activity:
			return JsonResponse({
				'status': 'fail',
				'err_code': 404,
				'err_info': 'no activity has id = ' + request.GET['id']
			})

		result = list(
			Person.objects.get(student_number = sn) for sn in activity.participator.split(',')
		)

		content = serializers.serialize('json', result)
		return HttpResponse(content, content_type = 'application/json')
