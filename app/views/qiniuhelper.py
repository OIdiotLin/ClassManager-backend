from django.http import HttpResponse
from django.http import JsonResponse

# Qiniu SDK
from qiniu import Auth

# Use when Http-Post
from django.views.decorators.csrf import csrf_exempt

# Use Token
from app.utils.token import token_check

import json
import classmanager.sensitive as key


@csrf_exempt
def get_upload_token(request):
	"""
	Get Upload token for Qiniu Storage
	:param request: Http-Post including args: filename
	:return: upload_token: Upload Token for upload `filename` on Qiniu
	"""
	if request.method == 'POST':
		if token_check(request):
			request_body = json.loads(request.body.decode('utf-8'))
			if 'filename' in request_body:

				filename = request_body['filename']

				# Generate Qiniu Authorization
				q = Auth(key.ACCESS_KEY, key.SECRET_KEY)

				# Generate Upload Token
				token = q.upload_token(key.BUCKET_NAME, filename, 3600)

				return JsonResponse({
					'status': 'success',
					'file_key': filename,
					'upload_token': token,
				})
			else:
				return JsonResponse({
					'status': 'fail',
					'err_code': 400,
					'err_info': 'argument `filename` missing'
				})
		else:
			return JsonResponse({
				'status': 'fail',
				'err_code': 400,
				'err_info': 'token check error'
			})
	else:
		return JsonResponse({
			'status': 'fail',
			'err_code': 400,
			'err_info': 'unacceptable request method'
		})
