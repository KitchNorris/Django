from django.urls import path, re_path

from . import views

app_name = 'polls'
urlpatterns = [
    path('ind/', views.ind, name='ind'),
    path('topics/', views.topics, name='topics'),
    re_path(r'^topic/(?P<topic_id>\d+)$', views.topic, name='topic'),
    re_path(r'^new_topic/$', views.new_topic, name='new_topic'),
    re_path(r'^new_entry/(?P<topic_id>\d+)$', views.new_entry, name='new_entry'),
    re_path(r'^edit_entry/(?P<entry_id>\d+)$', views.edit_entry, name='edit_entry'),
    path('uss/', views.uss, name='uss'),
    path('ussort/', views.ussort, name='ussort'),
    re_path(r'^userstops/(?P<us>\d+)$', views.userstops, name='userstops'),
    re_path('lenta/', views.lenta, name='lenta'),
    re_path('mark_as_read/', views.mark_as_read, name='mark_as_read')

]
