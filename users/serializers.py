from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','phone_number']
        # Note: Password kabhi bhi read serializer mein return nahi karte!

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password','phone_number']

        def create(self,validated_data):
            # User create karte waqt create_user function use karein taake password hash ho jaye
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                phone_number=validated_data.get['phone_number', '']
            )
            return user

        

        