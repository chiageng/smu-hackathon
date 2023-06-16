from django.shortcuts import render
from app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .utils import generate_files

# Create your views here.
def index(request):
    return render(request, 'app/index.html', {
                    
    })

def register(request):
    registered = False

    if (request.method == "POST"):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)  ## hash the password
            user.save()
        
            profile = profile_form.save(commit=False)  #dont save into database first
            profile.user = user  ## rmb profile and user is one to one relationship, so able to link back
        
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()
        
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else: 
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app/registration.html',
                {'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered})

def user_login(request):
    if request.method == "POST":
        username=request.POST.get("username")  # name is from form html name
        password = request.POST.get("password")
    
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('app:index'))
            
            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'app/login.html')

@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))


def upload(request):
    if request.method == "POST":
        template = TemplateUpload(request.POST, request.FILES)
        if template.is_valid():
            template.save()
            return HttpResponseRedirect(reverse("app:index"))
            
            

    else:
        template = TemplateUpload()
        # file = FileUpload()


        return render(request, "app/upload.html", {
            "template_form": template,
            # "file_form": file
            
        }) 
    
def generate(request):

    templates = TemplateFile.objects.all()
    files = File.objects.all()

    if request.method == "POST":
        form = GenerateForm(templates, files, request.POST)
        if form.is_valid():
            template_path = request.POST.get('template')
            data_path = request.POST.get('file')

            generate_files(template_path, data_path)

        return HttpResponseRedirect(reverse("app:index"))


    form = GenerateForm(templates, files)

    return render(request, 'app/generate.html', {
        # 'templates': templates,
        # 'files': files
        'form': form
    })