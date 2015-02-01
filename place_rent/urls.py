from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login,logout
from reserve.views import reserve,user
from place_rent.views import index

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'place_rent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login,{'extra_context':{'next':'/reserve/'}}),
    url(r'^accounts/logout/$',logout,{'extra_context':{'next':'/index/'}}),
	url(r'^reserve/$',reserve,name='reserve'),
	url(r'^user/$',user,name='user'),
	url(r'^',index,name='home'),
)
