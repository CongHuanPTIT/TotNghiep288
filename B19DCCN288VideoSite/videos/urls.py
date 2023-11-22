from django.urls import path
from .views import CreateVideo, DetailVideo, UpdateVideo, DeleteVideo, TopicVideo, SearchVideo

urlpatterns = [
    path('create/', CreateVideo.as_view(), name='video_create'),
    path('<int:pk>/', DetailVideo.as_view(), name='video_detail'),
    path('<int:pk>/update', UpdateVideo.as_view(), name='video_update'),
    path('<int:pk>/delete', DeleteVideo.as_view(), name='video_delete'),
    path('topic/<int:pk>', TopicVideo.as_view(), name='topic_list'),
    path('search/', SearchVideo.as_view(), name='search_video'),
]
