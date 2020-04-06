from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
        else:
            # if the data submitted is not valid, get the errors and save it to data
            data = serializer.errors

        return Response(data=data, status=status.HTTP_201_CREATED)
