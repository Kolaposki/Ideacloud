from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    # write_only so no one can see their passwords but only type em
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user_account = User(username=self.validated_data['email'], email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # check if the two passwords match before saving
        if password != password2:
            raise serializers.ValidationError({'password': "Hey, kindly check the passwords, seems they don't match"})

        user_account.set_password(password)
        user_account.save()
        return user_account
