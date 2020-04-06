from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer


@api_view(['POST'])
def api_registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user_account = serializer.save()  # save the ne account and get the details of the saved account
            data['response'] = f"User account created successfully for {user_account.username}"
            data['username'] = user_account.username
            data['email'] = user_account.email
            token = Token.objects.get(user=user_account).key  # get the token of that new user
            data['token'] = token
        else:
            # if the data submitted is not valid, get the errors and save it to data
            data = serializer.errors

        return Response(data=data)


# This helps in displaying the user token along with details when username and password are provided in headers
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
