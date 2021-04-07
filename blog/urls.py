from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('category/<str:cats>/', views.category, name='category'),
    path('category-list/', views.category_list, name='category-list'),
    path('category/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name='category-delete'),
    path('about/', views.about, name='about'),
    path('like/<int:pk>/', views.like, name='like_post'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]
