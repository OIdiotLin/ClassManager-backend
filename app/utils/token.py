# Extended string when generating tokens
from classmanager.sensitive import EXT_STRING

from django.http import JsonResponse

from hashlib import md5

# Used when http-POST
from django.views.decorators.csrf import csrf_exempt


def token_check(request):
	"""
	check tokens from client and server
	:param request: HttpRequest 
	:return: True: check succeeded
			False: check failed
	"""
	try:
		client_token = request.META.get('HTTP_TOKEN')

	except KeyError:
		client_token = ''

	server_token = generate_token(request)

	print('server-token: ' + server_token)
	print('client-token: ' + client_token)
	return client_token == server_token


def generate_token(request):
	"""
	Generate token from a http request
	:param request: HttpRequest (GET/POST)
	:return: token
	"""
	result = ''

	if request.method == 'GET':
		result = generate_token_get(request)

	if request.method == 'POST':
		result = generate_token_post(request)

	return result


def generate_token_get(request):
	"""
	Generate token from a GET request
	:param request: HttpRequest
	:return: md5
	"""
	keys = sorted(request.GET.keys())
	content = ''.join(key + request.GET[key] for key in keys)
	return encode_md5(content)


def generate_token_post(request):
	"""
	Generate token from a POST request
	:param request: HttpRequest
	:return: md5
	"""
	content = request.body.decode('utf-8')
	return encode_md5(content)


def encode_md5(plain_text):
	"""
	Encode the plain text by md5
	:param plain_text: 
	:return: cipher text
	"""
	plain_text = plain_text + EXT_STRING
	encoder = md5()
	encoder.update(plain_text.encode('utf-8'))
	return encoder.hexdigest()
