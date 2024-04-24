# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('add_todo/',add_todo),
    path('edit_todo/',edit_todo),
    path('delete_todo/',delete_todo),
    path('list_todo/',list_todo),
    path('view_todo/',view_todo),
    
    
]
