
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import *
class SysAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super(SysAdmin, self).create(validated_data)

