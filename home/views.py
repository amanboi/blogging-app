from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blogging.models import Post
# Create your views here.
def home(request):
    # Fetch top 3 blog post based on number of views
    # post = Post.objects.all()
    topPosts = Post.objects.order_by('-views')[:2]
    context = {'topPosts': topPosts}
    return render(request, 'home/home.html', context)


def about(request):
    # messages.success(request, "This is About")
    # return HttpResponse('This is about')
    return render(request, 'home/BLOG_About.html')

def contact(request):
    # messages.success(request, 'Welcome To Contact')
    if request.method=='POST':
      name = request.POST['name']
      email = request.POST['email']
      phone = request.POST['phone']
      content = request.POST['content']
      print(name,email,phone,content)

      if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
          messages.error(request, 'Please Fill The Form Correctly')
      else:
          contact = Contact(name=name,phone=phone,email=email,content=content) #   contact is object
          contact.save()
          messages.success(request, 'Your message has been sent')

      
      
     
    # return HttpResponse('This is contact')
    return render(request, 'home/BLOG_Contact.html')  


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()

    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
         messages.warning(request, 'No search result found please refine your query.')

    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    # return HttpResponse ('This is search')

def handleSignup(request):
    if request.method == 'POST':
        # GET THE POST PARAMETERS
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email= request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # Check For Errorneous Inputs
        # username should be under 10 chars
        # username should be alpha numeric
        # passwords should match
        if len(username) > 10:
            messages.error(request, "Your username must be under 10 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords Do Not Match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Should only have letters and numbers")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully")
        return redirect('home')



    else:
        return HttpResponse('404 -NOT FOUND')


def handleLogin(request):
    if request.method == 'POST':
        # GET THE POST PARAMETERS
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        

        else:
             messages.error(request, 'Invalid Credentials, Please try again')
             return redirect('home')
     
    return HttpResponse('404 -NOT FOUND')  

def handleLogout(request):
     logout(request)
     messages.success(request, 'Successfully Logged Out')
     return redirect('home')

     return HttpResponse(request, 'handleLogout')
    
       