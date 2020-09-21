from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import Contact
from blog.models import Post

# functions for handling html pages
def home(request):
    allPost = Post.objects.all()
    context = {'allPost':allPost}
    return render(request, 'home/home.html', context)

def contact(request):
    # django message framework is used.
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        if len(name) <=3 or len(email) <= 5 or len(content) <= 5:
            messages.error(request, 'Please mention complete details.')
        else:
            contact = Contact(name=name, email=email, content=content)
            contact.save()
            messages.success(request, 'Your query has been submitted successfully.')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    # searched query will be assigned to query variable(search tag's name must be query in html)
    # icontains is a django search functionality which searches a term in specified category(here title) with case-insensitivity
    query = request.GET['query']
    if len(query) > 50:
        allPosts = Post.objects.none()  # empty queryset
    
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
    
    if allPosts.count() == 0:
        messages.warning(request, 'No search result found. Try more general keywords.')       
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)

# functions for handling authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # get the post parameter
        username = request.POST['username']  # assigning the dictionary key's value to the variable
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # validating user input
        if len(username) <= 3:
            messages.error(request, "username must be grater than 3 characters.")
            return redirect('home')
        
        if not username.isalnum() :
            messages.error(request, "username should contain letters and numbers only.")
            return redirect('home')

        if not username.islower() :
            messages.error(request, "username should be in lower case letters.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords are not matching.")
            return redirect('home')

        # creating user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('home')
    else:
        return HttpResponse("Error found")        

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(request, username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully LoggedIn. Welcome {user.first_name} !!!")
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid Credentials. Please try again !')
            return redirect('home')


def handleLogout(request):
        logout(request)
        messages.success(request, "Successfully Logged Out.")
        return redirect('home')

