from django.conf.urls import url


from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register/$', views.register),
	url(r'^login/$', views.login),
	url(r'^tasks/$', views.home),
	# url(r'^tasks/process/$', views.process),
	# url(r'^tasks/toggle/$', views.toggle),
	url(r'^tasks/edit/$', views.edit),
	url(r'^tasks/delete/$', views.delete),
	url(r'^logout/$', views.logout),
]
