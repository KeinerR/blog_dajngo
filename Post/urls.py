
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create-post/', views.create_post, name='create_post'),
    path('post-store', views.post_store, name='post_store'),
    path('post/edit/<slug:slug>',views.post_edit,name="post_edit"),
    path('post/update/<slug:slug>',views.post_update,name="post_update")



]
