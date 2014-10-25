from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'mcnet.main.MainPage'),
	url(r'^/$', 'mcnet.main.MainPage'),
	url(r'^login/$', 'mcnet.main.login'),
	url(r'^logout/$', 'mcnet.main.logout'),
	url(r'^register/$', 'mcnet.main.register'),
	url(r'^cbase/$', 'mcnet.main.cbase'),
	url(r'^accounts/', include('allauth.urls')),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
