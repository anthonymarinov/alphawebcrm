from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def home(request):
    return render(request, 'public-pages/home.html', {})

def crm_home(request):
    records = Record.objects.all()

    # check if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('crm_home')
        else:
            messages.success(
                request, "There was an error logging in, please try again ...")
            return redirect('crm_home')
    else:
        return render(request, 'crm-pages/crm_home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully been logged out.")
    return redirect('crm_home')

def client_record(request, pk):
    if request.user.is_authenticated:
        # lookup record
        client_record = Record.objects.get(id=pk)
        return render(request, 'crm-pages/record.html', {'client_record': client_record})
    else:
        messages.success(request, "You must be logged in to view the page.")
        return redirect('crm_home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record successfully deleted.")
        return redirect('crm_home')
    else:
        messages.success(request, "You must be logged in to delete a record.")
        return redirect('crm_home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record successfully added.")
                return redirect('crm_home')
        return render(request, 'crm-pages/add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in.")
        return redirect('crm_home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record successfully updated.")
            return redirect('crm_home')
        return render(request, 'crm-pages/update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in.")
        return redirect('crm_home')
    
def about(request):
    return render(request, 'public-pages/about.html', {})

def services(request):
    return render(request, 'public-pages/services.html', {})

def projects(request):
    return render(request, 'public-pages/projects.html', {})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            human = True
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            project_subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_subject = f"{first_name} {last_name}: {project_subject}"
            full_message = (
                f"{first_name} {last_name}\n{email}\n{phone}\n{address}\n\n"
                f"{project_subject}\n\n{message}"
            )

            send_mail(
                email_subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['contact@alphamminc.com'],
                fail_silently=False,
            )

            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('contact')
        else:
            return render(request, 'public-pages/contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'public-pages/contact.html', {'form': form})