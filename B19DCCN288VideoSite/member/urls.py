from django.urls import path
from .views import MemberView, UpdateMemberView

urlpatterns = [
    path('<int:pk>/', MemberView.as_view(), name='member'),
    path('<int:pk>/update', UpdateMemberView.as_view(), name='update_member_info')
]
