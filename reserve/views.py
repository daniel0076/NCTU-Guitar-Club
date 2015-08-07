from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from reserve.models import staff,Records,Misc
from datetime import datetime
from reserve.place_rent_bot import *
from reserve.lottery import *
import re
from lxml import etree
from datetime import *
from operator import itemgetter

# Create your views here.

def index(request):
    return render(request,'index/index.html')
# use index/index.html to use the template in generic template folder rather than the one in the app

@login_required
def lottery(request):
    candidates,selected=select()
    return render(request,'lottery.html',locals())

@login_required
def settings(request):
    if 'ok' in request.POST:
        stuid =request.POST.get('stuid')
        name  =request.POST.get('name')
        phone =request.POST.get('phone')
        email =request.POST.get('email')
        staff.objects.create(name=name,email=email,phone=phone,stuid=stuid)

    if 'del' in request.POST:
        pid =request.POST.get('id')
        staff.objects.filter(id=pid).delete()

    staffs=staff.objects.order_by('stuid')

    return render(request,'settings.html',locals())
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
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

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

        #date validation
        book_date=datetime.strptime("{0}-{1}".format(year_month,date),"%Y-%m-%d")
        if datetime.today().date() >= book_date.date():
            res="日期錯誤，不能預約過去"
            return render(request,'send.html',{'res':res})

        data=book(contact_man,phone,email,stuid,act_name,place,year_month,date,time)
        updater()
        re_pattern="<script>alert\('(.*).{4}'\);</script>"
        if '資料庫語法錯誤' in data and 'alert' not in data:
            res="施法成功"
        else:
            warning=re.search(re_pattern,data)
            if warning is None:
                res="施法失敗，未知原因，請連絡idaniel.twc@gmail.com"
            else:
                res="施法失敗，{0}，請連絡idaniel.twc@gmail.com".format(warning.group(1))

        return render(request,'send.html',{'res':res})

def cancel(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    if 'ok' in request.POST:
        serial=request.POST.get('ser')
        Records.objects.filter(serial=serial).delete()
        data=make_cancel(serial)

        re_pattern="<script>alert\('(.*)'\);</script>"
        warning=re.search(re_pattern,data)
        if warning is None:
            res="Success"
        else:
            res="{0}".format(warning.group(1))

    return render(request,'send.html',locals())

def record(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    updated_time=Misc.objects.get().db_updated_time
    if datetime.now().date() > datetime.strptime(updated_time,"%Y-%m-%d").date():
        updater()

    record=Records.objects.order_by('date').reverse()
    return render(request,'record.html',locals())

@login_required
def update(request):
    updater()
    return HttpResponseRedirect('/record/')

def updater():
    data=get_record()
    page=etree.HTML(data)
    week=['一','二','三','四','五','六','日']
    #return list ['民謠之夜集訓', '四樓陽台', 'name', '0987654321', '2015-03-10', '晚上', '已完成借用手續']
    for it in page.xpath('//form'):
        ser=it.xpath('input')[0].get('value')
        item=it.xpath('tr/td/font//text()')
        item.append(ser)
        #item_day=datetime.strptime(item[4],"%Y-%m-%d").weekday()
        #item[4]+=" ({0})".format(week[item_day]) #weekday
        if not Records.objects.filter(serial=ser).exists():
            Records.objects.create(act_name=item[0].encode(),place=item[1].encode(),date=item[4].encode(),time=item[5].encode(),contact_man=item[2].encode(),status=item[6].encode(),serial=item[7].encode())

    Misc.objects.update_or_create(id=1,defaults={"db_updated_time":datetime.now().date()})
