from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from panel.views import home,initialization

# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user = auth.authenticate(username=user.username, password=password)
            if user is not None:
                auth.login(request, user)
                # messages.success(request,"Logged In Successfully")
                # docs = Doctor.objects.all()
                # for i in docs:
                #     if i.name == user:
                #         return redirect(doctorpanel.views.doctorhome)
                # p = Patient.objects.get(name=user)
                # if p.date_of_Birth == "" or p.height == 0 or p.weight == 0 or p.phoneno == "" or p.martial == "" :
                #     return redirect(completeprofile)
                # else:
                return redirect(home)
            else:
                messages.error(request,"Invalid Credentials")
        else:
            messages.error(request,"User does not exist.")
    context = {'title':"Login"}
    return render(request,'login.html',context)

def register(request):
    return None

def logout(request):
    auth.logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect(login)