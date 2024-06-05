from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.throttling import UserRateThrottle
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from users.forms import SignUpForm
User = get_user_model()

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            if User.objects.filter(email__iexact=email).exists():
                return render(request, 'signup.html', {'form': form, 'error': 'Email already exists.'})
            
            extract_name = email.splut('@')[0]
            user = User.objects.create_user(email=email,username=extract_name, password=password)
            user.save()
            login(request, user)
            return redirect('search')
        else:
            return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('search')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '')
        return User.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(username__icontains=keyword) | Q(email__iexact=keyword))

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([FriendRequestThrottle])
def send_friend_request(request):
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    receiver = User.objects.get(id=receiver_id)
    if sender != receiver:
        FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)
    return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def respond_to_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(id=pk, receiver=request.user)
        request_status = request.data.get('status')
        if friend_request.status != 'pending':
            return Response({"error": f"Friend request already {friend_request.status}."}, status=status.HTTP_400_BAD_REQUEST)
        elif request_status in ['accepted', 'rejected']:
            friend_request.status = request_status
            friend_request.save()
            return Response({"message": f"Friend request {request_status}."})
        return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(receiver=self.request.user, status='accepted')
        ).distinct()

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status='pending')
