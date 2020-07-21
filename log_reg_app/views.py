from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    return render(request, "welcome.html")

# DASHBOARD PAGE
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'cur_user': User.objects.get(id = request.session['user_id']),
        'users' : User.objects.all(),
        'all_jobs' : Job.objects.all().order_by('-created_at'),
    }
    return render(request, 'dashboard.html', context)

# REGISTRATION
def create(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        request.session.clear()
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['birth_date'] = request.POST['birth_date']
        request.session['email'] = request.POST['email']
        errors = User.objects.validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/register')
        new_user = User.objects.register(request.POST)
        request.session.clear()
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

# LOGIN
def login(request):
    if request.method == "GET":
        if 'first_name' in request.session:
            request.session.clear()
        return render(request, "login.html")
    else:
        result = User.objects.authenticate(request.POST['email'],request.POST['password']) # Checking login
        if result == False:
            messages.error(request, "Email or passwort do not match.")
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        return redirect('/login')

# LOGOUT
def logout(request):
    request.session.clear()
    return redirect("/login")

# VIEW JOB
def view_job(request, job_id):
    if len(Job.objects.filter(id = job_id)) > 0:
        context = {
            'cur_user': User.objects.get(id = request.session['user_id']),
            'needed_job':Job.objects.get(id = job_id)
        }
        return render(request, 'view_job.html', context)
    else:
        return redirect('/dashboard')



def create_new_job(request):
    if request.method == "GET":
        context = {
            'all_categories': Category.objects.all()
        }
        return render(request, "create_job.html", context)
    else:
        errors = Job.objects.job_validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/create_new_job')
        poster = User.objects.get(id = request.session['user_id'])
        
        this_job = Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'],poster = poster)
        categories = request.POST.getlist('category')
        if len(categories) > 0:
            for i in categories:
                needed_category = Category.objects.get(id = i)
                this_job.categories.add(needed_category)
                this_job.save()

        if len(request.POST['other']) > 0:
            cur_category = Category.objects.create(name = request.POST['other'])
            this_job.categories.add(cur_category)
            this_job.save()

        return redirect('/create_new_job')


def add_job(request, job_id):
    user = User.objects.get(id = request.session['user_id'])
    job = Job.objects.get(id =job_id)
    job.executor = user
    job.save()
    return redirect('/dashboard')

def done_job(request, job_id):
    job = Job.objects.get(id =job_id)
    job.delete()
    return redirect('/dashboard')

def giveup_job(request, job_id):
    user = User.objects.get(id = request.session['user_id'])
    job = Job.objects.get(id =job_id)
    job.executor = None
    job.save()
    return redirect('/dashboard')

# EDIT JOB
def edit_job(request, job_id):
    if request.method == "GET":
        context = {
            'cur_user': User.objects.get(id = request.session['user_id']),
            'needed_job': Job.objects.get(id = job_id),
            'all_categories': Category.objects.all()
        }
        return render(request, "edit_job.html", context)
    else:
        print(request.POST)
        errors = Job.objects.job_validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/create_new_job')
        edited_job = Job.objects.get(id = job_id)
        edited_job.title = request.POST['title']
        edited_job.description = request.POST['description']
        edited_job.location = request.POST['location']
        categories = request.POST.getlist('category')
        if len(categories) > 0:
            for i in categories:
                needed_category = Category.objects.get(id = i)
                edited_job.categories.add(needed_category)
                edited_job.save()
        edited_job.save()
        return redirect('/dashboard')

# REMOVE JOB
def remove_job(request, job_id):
    job = Job.objects.get(id =job_id)
    if job.poster.id == request.session['user_id']:
        job.delete()
    return redirect('/dashboard')

# REMOVE CATEGORY
def remove_category(request, category_id, job_id):
    category = Category.objects.get(id =category_id)
    job = Job.objects.get(id =job_id)
    if job.poster.id == request.session['user_id']:
        job.categories.remove(category)
        job.save()
    return redirect(f'/edit_job/{job_id}')
