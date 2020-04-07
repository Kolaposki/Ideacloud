from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .serializers import *
from users.models import User

"""
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

"""


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


# LoginView
class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(username=username, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = account.email
            context['username'] = username
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context)


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


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def api_registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) is not None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) is not None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# just a function to check if the email is not in the db. Will be called by api_registration_view
def validate_email(email):
    account = None
    try:
        account = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if account is not None:
        return email


# just a function to check if the username is not in the db. Will be called by api_registration_view
def validate_username(username):
    account = None
    try:
        account = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if account is not None:
        return username


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # Returns the object the view is displaying
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            new_password = serializer.data.get("new_password")
            old_password = serializer.data.get("old_password")
            confirm_new_password = serializer.data.get("confirm_new_password")

            # Check old password
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # check if new password is the same as old one
            if new_password == old_password:
                return Response({"new_password": ["Old password and new password can not be the same"]},
                                status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(new_password)
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# check if an account exist in the db
@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            account = User.objects.get(email=email)
            data['response'] = email
        except Account.DoesNotExist:
            data['response'] = "Account does not exist"
        return Response(data)
