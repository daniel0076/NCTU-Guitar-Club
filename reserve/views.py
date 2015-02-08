from django.shortcuts import render
from reserve.models import staff
from datetime import datetime
from reserve.place_rent_bot import *
import re
from lxml import etree
from datetime import *
from operator import itemgetter

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

        data=book(contact_man,phone,email,stuid,
                act_name,place,year_month,date,time)
        re_pattern="<script>alert\('(.*).{4}'\);</script>"
        if '資料庫語法錯誤' in data and 'alert' not in data:
            res="施法成功"
        else:
            warning=re.search(re_pattern,data)
            if warning is None:
                res="施法失敗，未知原因，請連絡管理員"
            else:
                res="施法失敗，{0}".format(warning.group(1))


        return render(request,'send.html',{'res':res})

def cancel(request):
    if not request.user.is_authenticated():
        return render(request,'index/index.html')

    if 'ok' in request.POST:
        serial=request.POST.get('ser')
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

    data=get_record()
    page=etree.HTML(data)
    week=['一','二','三','四','五','六','日']
    record=[]
    #return list ['民謠之夜集訓', '四樓陽台', 'name', '0987654321', '2015-03-10', '晚上', '已完成借用手續']
    for it in page.xpath('//form'):
        ser=it.xpath('input')[0].get('value')
        item=it.xpath('tr/td/font//text()')
        item.append(ser)
        item_day=datetime.strptime(item[4],"%Y-%m-%d").weekday()
        item[4]+=" ({0})".format(week[item_day]) #weekday
        record.append(item)
    records=sorted(record,key=itemgetter(4),reverse=True)
    return render(request,'record.html',locals())
