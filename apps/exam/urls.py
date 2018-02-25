from django.conf.urls import url


from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register/$', views.register),
	url(r'^login/$', views.login),
	url(r'^home/$', views.home),
	url(r'^home/process/$', views.process),
	url(r'^home/favorite/(?P<id>\d+)/$', views.favorite),
	url(r'^home/delete/(?P<id>\d+)/$', views.delete),
	url(r'^user/(?P<id>\d+)/$', views.user),
	url(r'^logout/$', views.logout),
]
