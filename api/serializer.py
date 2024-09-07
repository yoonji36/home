# api/serializer.py

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
        token['username'] = user.username
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

#[ 로그인 ]
#로그인 요청 보내기
# const handleLogin = async (email, password) => {
#     const response = await fetch('http://localhost:8000/api/login/', {
#         method: 'POST',
#         headers: {
#             'Content-Type': 'application/json',
#         },
#         body: JSON.stringify({ email, password }),
#     });

#     if (response.ok) {
#         const data = await response.json();
#         console.log('Login successful', data);
#          // 토큰 저장 및 사용자를 로그인 상태로 설정
#     } else {
#         console.error('Login failed');
#          // 에러 처리
#     }
# };