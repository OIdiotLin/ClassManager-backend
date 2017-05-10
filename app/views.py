from django.shortcuts import render

# Create your views here.


def show_api(request):
	return render(request, 'app/api.html')
