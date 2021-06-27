from django.contrib import admin
from django.urls import path
from . import views
app_name='post'
urlpatterns = [
  path('', views.all_post, name='all_posts'),
  path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
  path('add_post/<int:user_id>/',views.add_post,name='add_post'),
  path('post_delete/<int:user_id>/<int:post_id>/',views.post_delete,name='post_delete'),
  path('edit_post/<int:user_id>/<int:post_id>/',views.edit_post,name='edit_post'),
  path('Add_reply/<int:post_id>/<int:comment_id>/',views.Add_reply,name='Add_reply'),
  path('like/<int:post_id>/',views.like_post,name='like'),
]