from rest_framework import serializers
from app.users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            'id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'groups', 'user_permissions', 'activities',
            'last_login'
        ]
