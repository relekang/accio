from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^github', views.github, name='github')
]
