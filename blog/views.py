
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# from .forms import GeeksForm 
import bcrypt

# Create your views here.
# def home_view(request): 
#     context = {} 
#     context['form'] = GeeksForm() 
#     return render(request, "success.html", context) 

def index(request):
    return render(request, 'index.html',)

def goals(request):
    return render(request, 'Goals.html')

def projects(request):
    return render(request, 'projects.html')

def blog(request):
    return render(request, 'blog.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        'all_workouts': Workout.objects.all()
    }
    return render(request, 'success.html', context)

def register(request):
    errors = User.objects.reg_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags= key)
        return redirect('/')

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
    user.save()
    request.session['user_id'] = user.id
    return redirect('/success')

def add_workout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Workout.objects.workout_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/success')
    logged_in = User.objects.get(id=request.session['user_id'])
    new_workout = Workout.objects.create(
        title=request.POST['title'], description=request.POST['description'], instruction=request.POST['instruction'], posted_by=logged_in)
    new_workout.liked_by.add(logged_in)
    return redirect('/success')

def all_workouts(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['user_id']),
        'all_workouts': Workout.objects.all()
    }
    return render(request, 'success.html', context)

def one_workout(request, workout_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['user_id']),
        'one_workout': Workout.objects.get(id=workout_id)
    }
    return render(request, "one_workout.html", context)

# def my_favorites(request):
#     if 'user_id' not in request.session:
#         return redirect('/')
#     if Workout.liked_by == request.session['user_id']:
#         # context = {
#         #     'logged_user': User.objects.get(id=request.session['user_id']),
#         #     'my_favs' : Workout.objects.all()
#         # }
#         return redirect('/my_favorites.html')

def login(request):
    errors = User.objects.log_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        existing = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = existing.id
        return redirect('/success')


def edit_workout(request, workout_id):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Workout.objects.workout_val(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f"/success/{workout_id}")
    workout = Workout.objects.get(id=workout_id)
    workout.title = request.POST['title']
    workout.description = request.POST['description']
    workout.instruction = request.POST['instruction']
    workout.save()
    return redirect(f"/success")

def delete_workout(request, workout_id):
    if 'user_id' not in request.session:
        return redirect('/')
    workout = Workout.objects.get(id=workout_id)
    if workout.posted_by.id == request.session['user_id']:
        workout.delete()
    return redirect("/success")

def fav_workout(request, workout_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    workout = Workout.objects.get(id=workout_id)
    workout.liked_by.add(user)
    return redirect(f"/success/{workout_id}")


def unfav_workout(request, workout_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    workout= Workout.objects.get(id=workout_id)
    workout.liked_by.remove(user)
    return redirect(f"/success/{workout_id}")

def logout(request):
    request.session.clear()
    return redirect('/')