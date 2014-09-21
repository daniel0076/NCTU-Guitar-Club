from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'place_rent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^reserve/$','reserve.views.reserve',name='reserve'),
	url(r'^','index.views.index',name='home'),
)
