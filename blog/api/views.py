from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.models import Post
from users.models import User
from .serializers import PostSerializer


# API Read
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))  # Any user can read a blog (with or without having a token key)
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
@permission_classes((IsAuthenticated,))  # only user that's authenticated (has token key) can update a post
def api_update_blog_view(request, slug):
    try:
        # get the blog post based on the slug that was passed
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # Return a 404 if the blog post is not found
        return Response("This blog you seek for does not seem to exist!", status=status.HTTP_404_NOT_FOUND)

    user = request.user  # grab the user that's trying to update the post (will be gotten from the token key)

    if blog_post.author != user:
        # check if the authorized user is the author of the post
        return Response({'response': "You don't have permission to update this post, perhaps you're not the author"},
                        status=status.HTTP_401_UNAUTHORIZED)

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
@permission_classes((IsAuthenticated,))  # only user that's authenticated (has token key) can delete a post
def api_delete_blog_view(request, slug):
    try:
        # get the blog post based on the slug that was passed
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # Return a 404 if the blog post is not found
        return Response("This blog you seek for does not seem to exist!", status=status.HTTP_404_NOT_FOUND)

    user = request.user  # grab the user that's trying to delete the post (will be gotten from the token key)

    if blog_post.author != user:
        # check if the authorized user is the author of the post
        return Response({'response': "You don't have permission to delete this post, perhaps you're not the author"},
                        status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        operation = blog_post.delete()
        data = {}
        if operation:
            data["success"] = "Successfully deleted the post"
        else:
            data["failure"] = "Unable to delete post"

        return Response(data=data)


# API Create
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))  # only user that's authenticated (has token key) can create a post
def api_create_blog_view(request):
    account = request.user  # grab the user that's trying to create a post (will be gotten from the token key)
    blog_post = Post(author=account)

    if request.method == "POST":
        serializer = PostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Blog Post created successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to list all posts in d db, supports pagination
class ApiBlogListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'content', 'author__username')
