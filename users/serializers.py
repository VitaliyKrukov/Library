import re

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("id", "email", "phone", "password", "password_confirm", "avatar")

    def validate_email(self, value):
        """Валидация email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError("Некорректный формат email")
        return value

    def validate_password(self, value):
        """Валидация пароля."""
        if len(value) < 8:
            raise serializers.ValidationError(
                "Пароль должен содержать минимум 8 символов"
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву"
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну строчную букву"
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну цифру"
            )
        return value

    def validate(self, attrs):
        """Проверка совпадения паролей."""
        if attrs["password"] != attrs.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")  # Удаляем подтверждение пароля
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data,
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра/обновления профиля пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "avatar",
            "first_name",
            "last_name",
        )  # ДОБАВЛЕНО имя и фамилия
        read_only_fields = ("email",)  # Email нельзя менять

    def validate_phone(self, value):
        """Валидация номера телефона."""
        if value and not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise serializers.ValidationError("Некорректный формат номера телефона")
        return value

    def update(self, instance, validated_data):
        instance.phone = validated_data.get("phone", instance.phone)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance
