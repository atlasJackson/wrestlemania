from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('events/<slug:event>/', views.show_event , name='show_event'),
    path('events/<slug:event>/scorecard', views.event_scorecard , name='event_scorecard'),
    path('events/<slug:event>/scorecard/<int:id>', views.match_scorecard , name='match_scorecard'),

]