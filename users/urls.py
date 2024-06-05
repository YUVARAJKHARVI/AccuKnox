from django.urls import path
from .views import SignUpView, LoginView, UserSearchView, send_friend_request, respond_to_friend_request, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/search/', UserSearchView.as_view(), name='search'),
    path('api/friend-request/', send_friend_request, name='send_friend_request'),
    path('api/friend-request/<int:pk>/', respond_to_friend_request, name='respond_to_friend_request'),
    path('api/friends/', ListFriendsView.as_view(), name='list_friends'),
    path('api/pending-requests/', ListPendingRequestsView.as_view(), name='list_pending_requests'),
]
