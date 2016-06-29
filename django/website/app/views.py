from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Album,Song

# Create your views here.

def index(request):
	all_albums = Album.objects.all()
	context = {'all_albums':all_albums ,}
	return render(request,'app/index.html',context)

def detail(request,album_id):
	try:
		album = Album.objects.get(pk=album_id)
	except Album.DoesNotExist:
		raise Http404("Album Does Not Exist")
	return render(request,'app/detail.html',{'album' : album})

