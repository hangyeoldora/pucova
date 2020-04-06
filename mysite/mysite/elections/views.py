from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Candidate


# Create your views here.
def index(request):
    candidates = Candidate.objects.all()
    return render(request, 'elections/index.html')

@csrf_protect
def view(request):
    return render(request, 'elections/view.html',)


@csrf_protect
def get(request):
    area = request.POST.get('area')
    region = request.POST.get('region')
    if request.method=='POST':
        return render(request,'elections/get.html',{'area':area,"region":region})
    elif request.method=='GET':
        return render(request,'elections/get.html')

def about(request):
    area = request.POST.get('area')
    region = request.POST.get('region')
    if request.method=='POST':
        # return HttpResponse('POST method')
        # return render_to_response('elections/get.html')
        # return HttpResponse(request.POST.getlist('region'))
        return render(request,'elections/about.html',{'area':area,"region":region})
        return HttpResponseRedirect('elections/about.html')
    elif request.method=='GET':
        return render(request,'elections/about.html')
    return render(request,'elections/about.html')

