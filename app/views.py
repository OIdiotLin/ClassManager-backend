from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.db import DatabaseError

# Use Token
from .utils.token import token_check

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt

# Models
from .models import Person
from .models import Activity

# Create your views here.


def show_api(request):
	"""
	Show api list
	:param request: httpRequest
	:return: app/api.html
	"""
	return render(request, 'app/api.html')


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


def get_activity_list(request):
	"""
	Get activity list from MySQL databases
	:param request: HttpRequest
	:return: activity list (json)
	"""
	if request.method == 'GET' and token_check(request):

		data = Activity.objects.all()

		# if has filter
		if 'name' in request.GET:
			data = data.filter(name__contains = request.GET['name'])
		if 'content' in request.GET:
			data = data.filter(content__contains = request.GET['content'])

		content = serializers.serialize('json', data)
		return HttpResponse(content, content_type = 'application/json')


@csrf_exempt
def add_activity(request):
	"""
	Add new person into MySQL databases
	Http form MUST includes `name`, `date` and `time`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST' and token_check(request):

		try:
			new_activity = Activity(
				name = request.POST.get('name'),
				date = request.POST.get('date'),
				time = request.POST.get('time'),
				place = request.POST.get('place', ''),
				participation = request.POST.get('participation', 0),
				participator = request.POST.get('participator', ''),
				content = request.POST.get('content', ''),
				images = request.POST.get('images', '')
			)
			new_activity.save()

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
def delete_activity(request):
	"""
	Delete an activity by primary-key `id`
	Http form MUST includes `id`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
									doesn't exist	0
	"""
	if request.method == 'POST' and token_check(request):

		try:
			target_activity = Activity.objects.filter(
				id = request.POST.get('id')
			)
			if not target_activity.exists():
				return JsonResponse(
					{
						'status': 'fail',
						'err_code': 4004,
						'err_info': 'no object has id = ' + request.POST.get('id')
					}
				)
			target_activity.delete()
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
def update_activity(request):
	"""
	Update an activity in databases
	:param request: HttpRequest
	:return: status (success or fail), err_info and err_code
									doesn't exist	0
	"""
	if request.method == 'POST' and token_check(request):

		try:
			target_activity = Activity.objects.get(
				id = request.POST.get('target_id')
			)
			if not target_activity:
				return JsonResponse(
					{
						'status':   'fail',
						'err_code': 4004,
						'err_info': 'no object has id = ' + request.POST.get('target_id')
					}
				)
			# return JsonResponse(request.POST)

			for key in request.POST.keys():
				if not key == 'target_id':
					exec('target_activity.' + key + '=' + str(repr(request.POST.get(key))))
			target_activity.save()

			return JsonResponse({'status': 'success'})

		except DatabaseError as e:
			return JsonResponse(
				{
					'status': 'fail',
					'err_code': e.args[0],
					'err_info': e.args[1],
				}
			)
