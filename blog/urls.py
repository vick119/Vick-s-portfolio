from django.urls import path
from . import views
# from .views import home_view 

urlpatterns = [
    path('', views.index),
    path('Goals', views.goals),
    path('projects', views.projects),
    path('blog', views.blog),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('success', views.success),
    path('success', views.all_workouts),
    path('success/<int:workout_id>', views.one_workout),
    path('success/create', views.add_workout),
    path('success/<int:workout_id>/edit', views.edit_workout),
    path('success/<int:workout_id>/delete', views.delete_workout),
    path('success/<int:workout_id>/favorite', views.fav_workout),
    path('succes/<int:workout_id>/unfavorite', views.unfav_workout),
    # path('my_favorites', views.my_favorites),
    # path('success', views.home_view ), 
    # path('maps', views.maps),
]