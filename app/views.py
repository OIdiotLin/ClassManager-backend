from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

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


def parse_multi_filters(constraint_expressions, divider = '$'):
	"""
	Parse filters as a list from the constraint expressions string
	:param constraint_expressions: string
	:param divider: char between two constraint expression
	:return: filters (list)
	"""
	print(constraint_expressions.split(divider))
	return constraint_expressions.split(divider)


