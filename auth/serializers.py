from rest_framework import serializers
from django.contrib.auth.models import User
from auth.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE)
    phone_number = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type', 'phone_number']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        profile = user.profile
        profile.user_type = user_type
        profile.phone_number = phone_number
        profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')

        try:
            # محاولة إيجاد المستخدم إما عبر الإيميل أو رقم الجوال
            user = User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            try:
                user = User.objects.get(profile__phone_number=email_or_phone)
            except User.DoesNotExist:
                raise serializers.ValidationError(_("المستخدم غير موجود"))

        # تحقق من كلمة المرور
        if not user.check_password(password):
            raise serializers.ValidationError(_("كلمة المرور غير صحيحة"))

        if not user.profile.is_verified:
            raise serializers.ValidationError(_("الحساب غير مفعل"))

        data['user'] = user
        return data


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    token = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()
