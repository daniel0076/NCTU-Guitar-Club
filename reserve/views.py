from django.shortcuts import render
from reserve.models import staff

# Create your views here.
def reserve(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    return render(request,'reservation.html')

def index(request):
	return render(request,'index/index.html')
# use index/index.html to use the template in generic template folder rather than the one in the app


def user(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    s=staff.objects.all()
    return render(request,'user_list.html',locals())
