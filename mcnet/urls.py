from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'mcnet.main.MainPage'),
	url(r'^/$', 'mcnet.main.MainPage'),
	url(r'^index$', 'mcnet.main.MainPage'),
	url(r'^index.php$', 'mcnet.main.MainPage'),
	url(r'^login/$', 'mcnet.main.login'),
	url(r'^logout/$', 'mcnet.main.logout'),
	url(r'^register/$', 'mcnet.main.register'),
	url(r'^cbase/$', 'mcnet.main.cbase'),
	url(r'^cp/$', 'mcnet.main.database_controlpanel'),
	url(r'^addEdition/$', 'mcnet.main.addEdition'),
	url(r'^importEditions/$', 'mcnet.main.importEditions'),
	url(r'^importCards/$', 'mcnet.main.importCards'),
	url(r'^cardInfo/$', 'mcnet.main.cardInfo'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
