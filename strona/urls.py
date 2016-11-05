from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.map_view, name='index'),
    url(r'^time_chart/$', views.time_chart_view, name='time_chart'),
    url(r'^correlation_chart/$', views.correlation_chart_view, name='correlation_chart'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
