from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()


    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #login user
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in - please try again..."))
            return redirect('home')

    else:
        return render(request,'home.html', { 'records': records})

#def login_user(request):
    #pass

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #save user
            form.save()
            #get username and password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #authenticate user
            user = authenticate(username=username, password=password)
            #login user
            login(request, user)
            messages.success(request, ("You have been registered!"))
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request,'register.html', {'form': form, 'title': 'Register'})

    return render(request,'register.html', {'form': form, 'title': 'Register'})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, ("Please login to view customer records..."))
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ("Customer record deleted..."))
        return redirect('home')
    else:
        messages.success(request, ("Please login to delete customer records..."))
        return redirect('home')

def add_record(request):

    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, ("Customer record added..."))
                return redirect('home')


        return render(request, 'addRecord.html', {'form': form})
    else:
        messages.success(request, ("Please login to add customer records..."))
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, ("Customer record updated..."))
                return redirect('home')

        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, ("Please login to update customer records..."))
        return redirect('home')
