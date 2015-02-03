from django.shortcuts import render
from reserve.models import staff
from datetime import datetime
from reserve.place_rent_bot import *

# Create your views here.

def index(request):
	return render(request,'index/index.html')
# use index/index.html to use the template in generic template folder rather than the one in the app


def reserve(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    nowy=datetime.now().year
    nowm=datetime.now().month
    year_month=[ str(nowy)+"-"+str(m).zfill(2) for m in range (nowm,13) ]
    if nowm > 8:
        year_month.extend( [ str(nowy+1)+"-"+str(m).zfill(2) for m in range (1,7) ] )
    days=[ d for d in range(1,32) ]
    s=staff.objects.all()
    return render(request,'reservation.html',locals())

def send(request):

    if 'ok' in request.POST:
        contact_id  =request.POST.get('contact')
        contact     =staff.objects.get(id=contact_id)
        contact_man =contact.name;
        phone       =contact.phone;
        email       =contact.email;
        stuid       =contact.stuid;
        act_name    =request.POST.get('act_name')
        place       =request.POST.get('place')
        year_month  =request.POST.get('year_month')
        date        =request.POST.get('date')
        time        =request.POST.get('time')

        data=book(contact_man,phone,email,stuid,
                act_name,place,year_month,date,time)
        if '資料庫語法錯誤' in data and 'alert' not in data:
            res="預約成功"
        else:
            res="預約失敗"


        return render(request,'send.html',locals())

