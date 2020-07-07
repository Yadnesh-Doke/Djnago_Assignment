# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import requests
import json

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from Covid_cases.models import Cases,Country

def login_view(request):
    # Cases.objects.all().delete()
    # world = requests.get("https://covid-19.dataflowkit.com/v1/world")
    # world = world.json()

    # cases = Cases.objects.create(
    #                             total_confirmed = int(world["Total Cases_text"].replace(",","")),
    #                             total_recovered = int(world["Total Recovered_text"].replace(",","")),
    #                             total_deaths = int(world["Total Deaths_text"].replace(",","")),
    #                             newly_confirmed = int(world["New Cases_text"].replace(",","")),
    #                             newly_deaths = int(world["New Deaths_text"].replace(",","")),
    #                             active_cases = int(world["Active Cases_text"].replace(",",""))
    #                             )

    # # print(cases)
    # cases.save()

    # countries1 = ["USA","brazil","russia","india","mexico","pakistan"]
    # countries2 = ["UK","spain","peru","chile","italy","iran","turkey","saudi arabia","germany"]
    # # countries3 = ["peru","chile","italy","iran","turkey","saudi arabia","germany"]

    # Country.objects.all().delete()

    # for country in countries1:
    #     country_cases = requests.get("https://covid-19.dataflowkit.com/v1/" + country)
    #     country_cases = country_cases.json()
    #     if (country_cases["New Cases_text"].replace(",","")) == "":
    #         country_cases["New Cases_text"] = "0"

    #     if (country_cases["New Deaths_text"].replace(",","")) == "":
    #         country_cases["New Deaths_text"] = "0"

    #     cases_obj = Cases(
    #                       total_confirmed = int(country_cases["Total Cases_text"].replace(",","")),
    #                       total_recovered = int(country_cases["Total Recovered_text"].replace(",","")),
    #                       total_deaths = int(country_cases["Total Deaths_text"].replace(",","")),
    #                       newly_confirmed = int(country_cases["New Cases_text"].replace(",","")),
    #                       newly_deaths = int(country_cases["New Deaths_text"].replace(",","")),
    #                       active_cases = int(country_cases["Active Cases_text"].replace(",",""))
    #     )
    #     cases_obj.save()
    #     if country_cases["Country_text"].upper() == "USA":
    #         print("FROM AUTHENTICATION, USA=",country_cases["Country_text"])
    #     country_obj = Country(country_name=country_cases["Country_text"].capitalize(),cases=cases_obj)
    #     country_obj.save()

    # for country in countries2:
    #     country_cases = requests.get("https://api.covid19api.com/total/country/" + country)
    #     country_cases = country_cases.json()[-1]
    #     cases_obj = Cases(
    #                       total_confirmed = int(country_cases["Confirmed"]),
    #                       total_recovered = int(country_cases["Recovered"]),
    #                       total_deaths = int(country_cases["Deaths"]),
    #                       newly_confirmed = 0,
    #                       newly_deaths = 0,
    #                       active_cases = int(country_cases["Active"])
    #     )
    #     cases_obj.save()

    #     country_obj = Country(country_name=country_cases["Country"].capitalize(),cases=cases_obj)
    #     country_obj.save()

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
