from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.models import User
from myapp.models import User, Product


class ProductSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # username = serializers.CharField(
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

