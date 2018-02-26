
from django.contrib import admin
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^posts/(?P<post_url>[\w-]+)$', views.detail),
    url(r'^home/$', views.home),
    url(r'^login/$', views.login_view),
    url(r'^calc/$', views.calc),
    url(r'^signup/$', views.signup_view),
    url(r'^profile/(?P<uid>[\w-]+)/$$', views.profile),
    url(r'^upvote/(?P<post_url>[\w-]+)/$', views.upvote),
    url(r'^submit_comment/(?P<post_url>[\w-]+)$', views.submit_comment),
    #url(r'^(?P<size>[\w-]+)/(?P<color>.*)$', views.image),


]