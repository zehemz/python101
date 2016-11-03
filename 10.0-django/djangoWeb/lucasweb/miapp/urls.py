'''
Generado por Lucas
'''
from django.conf.urls import url
from . import views #Estoy importando a que funcion llamar.
app_name = 'miapp'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    #url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #ex: admin/miapp/contact/4/change/images/nombre.../change/
    #admin/miapp/contact/4/change/images/FlICmGnj.jpeg/change/
    url(r'^admin/miapp/contact/(?P<contact_id>[0-9]+)/change/images/(?P<file_name>)/change/$', views.image, name='image')
]
