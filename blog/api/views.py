from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blog.models import Post
from users.models import User
from .serializers import PostSerializer


# API Read
@api_view(['GET'])
def api_detail_blog_view(request, slug):
    try:
        # get the blog post based on the slug that was passed
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # Return a 404 if the blog post is not found
        return Response("This blog you seek for does not seem to exist!", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(blog_post)  # serialize the blog post by turning it into a json format
        return Response(serializer.data, status=status.HTTP_200_OK)


# API Update
@api_view(['PUT'])
def api_update_blog_view(request, slug):
    try:
        # get the blog post based on the slug that was passed
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # Return a 404 if the blog post is not found
        return Response("This blog you seek for does not seem to exist!", status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = PostSerializer(blog_post, data=request.data)  # serialize the post along with the new passed data
        data = {}
        if serializer.is_valid():
            serializer.save()  # save the new data if all fields are valid and update the post
            data["success"] = 'Successfully updated the post'
            return Response(data=data, status=status.HTTP_200_OK)

        # return whatever errors got from the server along with a 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API Delete
@api_view(['DELETE'])
def api_delete_blog_view(request, slug):
    try:
        # get the blog post based on the slug that was passed
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # Return a 404 if the blog post is not found
        return Response("This blog you seek for does not seem to exist!", status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = blog_post.delete()
        data = {}
        if operation:
            data["success"] = "Successfully deleted the post"
        else:
            data["failure"] = "Unable to delete post"

        return Response(data=data)
