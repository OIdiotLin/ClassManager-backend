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
from app.models import Activity
from app.models import Person


def get_activity_list(request):
	"""
	Get activity list from MySQL databases
	:param request: HttpRequest
	:return: activity list (json)
	"""
	if request.method == 'GET':

		data = Activity.objects.all()

		# if has filter
		if 'name' in request.GET:
			data = data.filter(name__contains = request.GET['name'])
		if 'content' in request.GET:
			data = data.filter(content__contains = request.GET['content'])

		content = [dict(x) for x in data.values()]

		return JsonResponse({
			'count': data.count(),
			'result': content
		})


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

			participators = new_activity.participator.split(',')

			for stu_num in participators:
				person = Person.objects.get(student_number = stu_num)
				person.participation += int(new_activity.participation)
				person.save()

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
						'err_code': 404,
						'err_info': 'no object has id = ' + request.POST.get('id')
					}
				)

			participators = target_activity.first().participator.split(',')

			for stu_num in participators:
				person = Person.objects.get(student_number = stu_num)
				person.participation -= int(target_activity.first().participation)
				person.save()

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
				id = request.POST.get('id')
			)
			if not target_activity:
				return JsonResponse(
					{
						'status':   'fail',
						'err_code': 404,
						'err_info': 'no object has id = ' + request.POST.get('id')
					}
				)

			original_participation = int(target_activity.participation)
			current_participation = int(
				request.POST.get('participation')
				if 'participation' in request.POST.keys() else original_participation
			)

			original_participators = set(target_activity.participator.split(','))
			current_participators = set(
				request.POST.get('participator').split(',')
				if 'participator' in request.POST.keys() else original_participators
			)

			added_participators = current_participators - original_participators
			removed_participators = original_participators - current_participators

			if not current_participation == original_participation:
				for stu_num in original_participators:
					person = Person.objects.get(student_number = stu_num)
					person.participation += current_participation - original_participation
					person.save()

			for stu_num in added_participators:
				person = Person.objects.get(student_number = stu_num)
				person.participation += current_participation
				person.save()

			for stu_num in removed_participators:
				person = Person.objects.get(student_number = stu_num)
				person.participation -= current_participation
				person.save()

			for key in request.POST.keys():
				if not key == 'id':
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
