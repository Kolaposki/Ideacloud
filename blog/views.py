from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CommentForm, PostForm


# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', context={'posts': posts})


# Using Class based view
#     ListView — to view the list of objects
#     CreateView — to create a particular object
#     DetailView — to view a particular object
#     UpdateView — to update a particular object
#     DeleteView — to delete a particular object


# View list of all posts
class PostListView(ListView):
    model = Post  # The model to query
    template_name = 'home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # name of object query
    ordering = ['-date_posted']  # order by the date posted but in reverse order cuz of '-'
    paginate_by = 5


# View list of all posts from a specific author/user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering is done by the filter below
    paginate_by = 5

    # a method to filter posts by a single author/user
    def get_queryset(self):
        # return 404 if that user/author doesn't exist
        # grab the objects from User model
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # get the username from the url
        return Post.objects.filter(author=user).order_by('-date_posted')  # filter all posts if the author == user


'''
# a view to display a single detailed post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # conventional name for 'context_object_name' is 'object' so....i'll be using object instead of 'posts'
'''


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # queryset to retrieve all the approved comments from the database.
    comments = post.comments.filter(active=True).order_by("-created_on")[0:5]
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)  # hold data entered by the user
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     })


# a view to create a single post. Form included
# LoginRequiredMixin : Only authenticated users can create a new post | Will redirect to login page if not auth
class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    # fields = ['title', 'content', 'cover']  # form fields to be added in order
    template_name = 'blog/post_form.html'  # convention name
    success_message = "Post was successfully created"

    form_class = PostForm  # where to get the form to render in page

    # update_cover = Post(request.POST, request.FILES, instance=request.cover)

    # success_url : url to redirect to after successfully submiting a new post

    # overide form valid method and tell what to do after submiting form
    def form_valid(self, form):
        # form.save_m2m()  # to save tags
        form.instance.author = self.request.user  # set the current logged in user as the author of the post
        # update_cover.save()
        return super().form_valid(form)  # validate the form and submit


# UserPassesTestMixin : To ensure the creator of the post is the one updating it
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # fields = ['title', 'content', 'cover']
    form_class = PostForm
    template_name = 'blog/post_update.html'

    # no need of a template_name since the post being viewed is d one to b updated

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully")
        return super().form_valid(form)

    # test to see if a user passes a certain condition
    # ensure that only the author of a post can edit the post
    def test_func(self):
        post = self.get_object()  # get the exact current opened post
        if self.request.user == post.author:  # if the logged in user is the same as the author of the current post
            return True
        return False


# delete a particular post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # redirect after deleting post '/' for home
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            # messages.info(self.request, "Post was deleted")
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


# filters all posts with the specific tag
def tag_posts(request, tags):
    # posts = Post.objects.filter(tagged_items=tags)
    # url_tag = str(request.GET('tags')).lower
    # tag = get_object_or_404(Tag, tags)  # get the tags from the url
    posts = Post.objects.filter(tags__name__in=[tags]).distinct()
    context = {
        'posts': posts,
        'post_tag': tags,
    }
    return render(request, 'blog/tag_posts.html', context)


# filters all posts with the specific category
class PostCategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        categories = get_object_or_404(Category, name=self.kwargs.get('categories'))  # get the category from the url
        return Post.objects.filter(category=categories).order_by(
            '-date_posted')

