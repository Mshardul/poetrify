from django.conf.urls import url

from poetrify import views

urlpatterns = [
    url(r'^getRhymes', views.RhymesRequest, name='RhymesRequest'),
    url(r'^home$', views.Home, name='Home'),
    url(r'^addNewWords', views.AddNewWords, name="AddNewWords"),
    url(r'^addNewRhymes', views.AddNewRhymes, name="AddNewRhymes"),
    url(r'^getNoOfRequests', views.GetNoOfRequests, name="GetNoOfRequests"),
    url(r'^requests', views.Requests, name="Requests"),
    url(r'^getRequest', views.GetRequest, name="GetRequest"),
    url(r'^requestApproval', views.RequestApproval, name="RequestApproval"),
    url(r'^seeAll', views.SeeAll, name="SeeAll"),
    url(r'^trial', views.Trial, name="trial"),
]