from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login,logout
from django.core.urlresolvers import reverse
from reserve.views import reserve,send,record,cancel
from place_rent.views import index

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'place_rent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^accounts/login/$',login,name='login'),
    url(r'^accounts/logout/$',logout,name='logout'),
    url(r'^reserve/$',reserve,name='reserve'),
    url(r'^send/$',send,name='send'),
    url(r'^record/$',record,name='record'),
    url(r'^cancel/$',cancel,name='cancel'),
    url(r'^',index,name='home'),
)
