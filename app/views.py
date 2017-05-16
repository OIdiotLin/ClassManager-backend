from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.db import DatabaseError

from django.forms.models import model_to_dict

# Use Regular Expression
import re

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

		# if has filter
		if 'filter' in request.GET:
			data = Person.objects.all().extra(
				where = parse_multi_filters(request.GET['filter'])
			)
			content = serializers.serialize("json", data)
			return HttpResponse(content, content_type = 'application/json')

		# if requires all
		else:
			data = Person.objects.all()
			content = serializers.serialize("json", data)
			return HttpResponse(content, content_type = 'application/json')


@csrf_exempt
def add_person(request):
	"""
	Add new person into MySQL databases
	Http form MUST includes `student_number`, `name`, `pinyin` and `gender`
	:param request: httpRequest
	:return: status (success or fail), err_info and err_code
	"""
	if request.method == 'POST':

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
	if request.method == 'POST':

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
	if request.method == 'POST':

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


def parse_multi_filters(constraint_expressions, divider = '$'):
	"""
	Parse filters as a list from the constraint expressions string
	:param constraint_expressions: string
	:param divider: char between two constraint expression
	:return: filters (list)
	"""
	return constraint_expressions.split(divider)


