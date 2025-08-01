import json
from pyexpat.errors import messages
from sqlite3 import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from functools import wraps
from django.contrib import messages  
from django.db.models import Q, Avg
import random

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')