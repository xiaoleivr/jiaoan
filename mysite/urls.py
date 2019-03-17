from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('center/', views.dashboard, name='dashboard'),
    path('register/',views.register,name='register'),
    path('', include('django.contrib.auth.urls')),

    path('profiles/', views.ProfileList.as_view(), name='pro_list'),
    path('profile/edit/', views.profileedit, name='pro_edit'),
    path('profile/<pk>/', views.ProfileDetail.as_view(), name='pro_detail'),

    path('like/', views.user_like, name='like'),
    path('user_chk/',views.user_chk,name='user_chk'),

    path('posts/catgory/<int:id>/',views.catposts,name='posts_by_cat'),
    path('posts/auth/<int:id>/',views.authposts,name='posts_by_user'),
    path('post/create/',views.PostCreate.as_view(),name='post_create'),
    path('post/comment/',views.post_comment,name='post_comment'),
    path('post/<year>/<month>/<day>/<slug>/',views.PostDetail.as_view(),name='post_detail'),
]

