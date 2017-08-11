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

import json


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
			activity_info = json.loads(request.body.decode('utf-8'))['activity']

			new_activity = Activity(
				name = activity_info['name'],
				date = activity_info['date'],
				time = activity_info['time'],
				place = activity_info['place'] if 'place' in activity_info.keys() else '',
				participation = activity_info['participation'] if 'participation' in activity_info.keys() else 0,
				participator = activity_info['participator'] if 'participator' in activity_info.keys() else '',
				content = activity_info['content'] if 'content' in activity_info.keys() else '',
				images = activity_info['images'] if 'images' in activity_info.keys() else ''
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
			activity_info = json.loads(request.body.decode('utf-8'))['activity']

			target_activity = Activity.objects.filter(
				id = activity_info['id']
			)
			if not target_activity.exists():
				return JsonResponse({
						'status': 'fail',
						'err_code': 404,
						'err_info': 'no object has id = ' + activity_info['id']
				})

			participators = target_activity.first().participator.split(',')

			if participators[0] != '':
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
			target_id = json.loads(request.body.decode('utf-8'))['target_id']
			activity_info = json.loads(request.body.decode('utf-8'))['activity']

			target_activity = Activity.objects.get(
				id = target_id
			)
			if not target_activity:
				return JsonResponse(
					{
						'status':   'fail',
						'err_code': 404,
						'err_info': 'no object has id = ' + target_id
					}
				)

			original_participation = int(target_activity.participation)
			current_participation = int(
				activity_info['participation']
				if 'participation' in activity_info.keys() else original_participation
			)

			original_participators = set(filter(None, target_activity.participator.split(',')))
			current_participators = set(
				filter(None, activity_info['participator'].split(','))
				if 'participator' in activity_info.keys() else original_participators
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

			for key in activity_info.keys():
				if not key == 'id':
					exec('target_activity.' + key + '=' + str(repr(activity_info[key])))

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
