from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method == 'POST':  # if some data is sumbitted through the form
        # request.POST['username'] = str(request.POST['username']).lower()
        form = UserRegisterForm(request.POST)  # create an instance of the data submitted through the form

        if form.is_valid():  # if the data submitted through the form is valid]
            form.save()  # save the data to the DB
            username = form.cleaned_data.get('username')  # get the username of the user
            messages.success(request, f'Account for {username} created successfully!')  # display a success message
            return redirect('login')  # go back to login page to confirm registration

        elif not form.is_valid():
            # messages.warning(request, 'Unable to create user account')
            messages.get_messages(request)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required  # redirects user if user tries to access profile without being authenticated
def profile(request):
    if request.method == 'POST':
        # instance : to show current logged in user username & email in the edit form (placeholder)
        # request.POST : to populate the db with the filled in data
        update_form = UserUpdateForm(request.POST, instance=request.user)

        # instance : to show current logged in user pic
        # request.FILES : to handle the uploaded file
        update_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if update_form.is_valid() and update_profile.is_valid():
            update_profile.save()
            update_form.save()

            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)
        update_profile = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': update_form,
        'u_profile': update_profile
    }
    return render(request, 'users/profile.html', context=context)
