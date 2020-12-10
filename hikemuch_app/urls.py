from django.urls import path
from . import views
from .views import HikeCreateView, edit_hike, delete_hike, like_hike, add_comment_to_hike

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.hike_details, name="hike details"),
    path('<int:pk>/<str:slug>/', views.hike_details, name="hike details"),
    path('create/', HikeCreateView.as_view(), name='create'),
    path('edit/<int:pk>', edit_hike, name='edit hike'),
    path('delete/<int:pk>', delete_hike, name='delete hike'),
    path('like/<int:pk>/', like_hike, name='like hike'),
    path('comment/<int:pk>/', add_comment_to_hike, name='add_comment_to_hike'),
]
