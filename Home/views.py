from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request,'Home/index.html') 

# Create your views here.
def AboutUs(request):
    return render(request,'Home/about_us.html') 

# Create your views here.
def Services(request):
    return render(request,'Home/service.html') 