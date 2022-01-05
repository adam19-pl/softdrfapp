from django.urls import path
from drfapp import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('logout/blacklist/',views.BlackListTokenView.as_view(),name='blacklist')
]

