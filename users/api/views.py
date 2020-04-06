from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.models import User


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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_detail_view(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response({"response": "This user doesn't seem to exist in the database"},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AccountDetailsSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_user_view(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response({"response": "This user doesn't seem to exist in the database"},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = AccountDetailsSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account updated successfully"
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
