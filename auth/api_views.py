from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import *
from auth.models import Profile
import random
import string
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.profile.user_type,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'تم التسجيل بنجاح'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user:
            return Response({'message': 'تم تسجيل الدخول بنجاح'}, status=status.HTTP_200_OK)
        return Response({'error': 'بيانات الدخول غير صحيحة'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def forget_password(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            profile = Profile.objects.get(email=email)
            token = ''.join(random.choices(string.digits, k=4))
            profile.forget_password_token = token
            profile.save()
            # يمكن إرسال التوكن بالبريد/رسالة هنا
            return Response({'token': token}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'البريد الإلكتروني غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def verify_token(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        try:
            profile = Profile.objects.get(forget_password_token=token)
            return Response({'message': 'رمز التحقق صحيح'}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'رمز غير صالح'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        try:
            profile = Profile.objects.get(forget_password_token=token)
            user = profile.user
            user.set_password(new_password)
            user.save()
            profile.forget_password_token = None
            profile.save()
            return Response({'message': 'تم تغيير كلمة المرور'}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'رمز غير صالح'}, status=status.HTTP_400_BAD_REQUEST)
