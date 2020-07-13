# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import requests
import json


from json import dumps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from Covid_cases.models import Cases,Country
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.conf import settings

import time, threading

StartTime=time.time()
selected_country_for_updates = ""
email = ""
update_mails = {}

def action() :
    ''' for sending the email updates to the subscribed users for their selected countries '''
    if len(update_mails) != 0:
        print("length of dict:")
        print(len(update_mails))
        for email in update_mails:
            for country in update_mails[email]:
                print("CURRENT MAIL: ",email)
                print("CURRENT COUNTRY: ",country)
                subject = f"Today's updates for the covid-19 cases for {country}"
                
                selected_country = Country.objects.get(country_name=country)
                confirmed = selected_country.cases.total_confirmed
                recovered = selected_country.cases.total_recovered
                deaths = selected_country.cases.total_deaths
                message = f"{country}:\n Total confirmed cases : {confirmed} \n Total Recovered cases : {recovered} \n Total Death cases : {deaths}\n"
                print("MESSAGE")
                print(message)
                send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False)
                print("Email sent from THIS")

    else:
        print("No one has subscribed.")


class setInterval :
    ''' To periodically call a method (in this case, action()) '''
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

# start action every 30s
inter=setInterval(30,action)

#will stop interval in 90s
t=threading.Timer(90,inter.cancel)
t.start()


@login_required(login_url="/login/")
def index(request):
    print("INSIDE INDEX.HTML")
    Cases.objects.all().delete()
    #fetching worldwide stats through api and storing in the database
    world = requests.get("https://covid-19.dataflowkit.com/v1/world")
    world = world.json()

    cases = Cases.objects.create(
                                total_confirmed = int(world["Total Cases_text"].replace(",","")),
                                total_recovered = int(world["Total Recovered_text"].replace(",","")),
                                total_deaths = int(world["Total Deaths_text"].replace(",","")),
                                newly_confirmed = int(world["New Cases_text"].replace(",","")),
                                newly_deaths = int(world["New Deaths_text"].replace(",","")),
                                active_cases = int(world["Active Cases_text"].replace(",",""))
                                )

    cases.save()

    countries1 = ["USA","brazil","india","russia","peru","chile","mexico","iran","italy","pakistan","south africa","saudi arabia","turkey","germany"]
    countries2 = ["UK","spain"]

    Country.objects.all().delete()

    #fetching statistics for countries and storing in the database table
    for country in countries1:
        country_cases = requests.get("https://covid-19.dataflowkit.com/v1/" + country)
        country_cases = country_cases.json()
        if (country_cases["New Cases_text"].replace(",","")) == "":
            country_cases["New Cases_text"] = "0"

        if (country_cases["New Deaths_text"].replace(",","")) == "":
            country_cases["New Deaths_text"] = "0"

        cases_obj = Cases(
                          total_confirmed = int(country_cases["Total Cases_text"].replace(",","")),
                          total_recovered = int(country_cases["Total Recovered_text"].replace(",","")),
                          total_deaths = int(country_cases["Total Deaths_text"].replace(",","")),
                          newly_confirmed = int(country_cases["New Cases_text"].replace(",","")),
                          newly_deaths = int(country_cases["New Deaths_text"].replace(",","")),
                          active_cases = int(country_cases["Active Cases_text"].replace(",",""))
        )
        cases_obj.save()
        country_obj = Country(country_name=country_cases["Country_text"].capitalize(),cases=cases_obj)
        country_obj.save()

    for country in countries2:
        country_cases = requests.get("https://api.covid19api.com/total/country/" + country)
        country_cases = country_cases.json()
        country_cases = country_cases[-2]
        cases_obj = Cases(
                          total_confirmed = int(country_cases["Confirmed"]),
                          total_recovered = int(country_cases["Recovered"]),
                          total_deaths = int(country_cases["Deaths"]),
                          newly_confirmed = 0,
                          newly_deaths = 0,
                          active_cases = int(country_cases["Active"])
        )
        cases_obj.save()
        
        country_obj = Country(country_name=country_cases["Country"].capitalize(),cases=cases_obj)
        country_obj.save()


    #setting the context dictionary so that data can be used in templates
    world = Cases.objects.all()[0]
    fatality_rate = ((world.total_deaths) / (world.total_confirmed)) * 100
    recovery_rate = ((world.total_recovered) / (world.total_confirmed)) * 100
    context = {"world" : world,"fatality_rate":fatality_rate,"recovery_rate":recovery_rate}
    country_codes = {"usa":'us',"brazil":'br',"russia":'ru',"india":'in',"mexico":'mx',"pakistan":'pk',"united kingdom":'gb',
                     "spain":'es',"peru":'pe',"chile":'cl',"italy":'it',"iran":'ir',"turkey":'tr',"saudi arabia":'sa',"germany":'de'}

    country_deaths = Country.objects.all().order_by("-cases__total_deaths")[:3]
    i = 1
    for country in country_deaths:
        context["country"+str(i)] = country
        death_rate = ((country.cases.total_deaths) / (country.cases.total_confirmed)) * 100
        context["country"+str(i)+"_deathRate"] = death_rate
        context["country"+str(i)+"_code"] = "/static/assets/img/flags/" + country_codes[country.country_name.lower()]+".png"
        i += 1

    print("LEAVING INDEX.HTML")
    return render(request, "index.html",context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    countries = Country.objects.all()
    countries_dict = {}
    for country in countries:
        countries_dict[(country.country_name.capitalize())] = (country.__str__())

    #setting up the context so that relevant data of countries can be used in template files for rendering
    context["countries"] = countries_dict

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def subscribe(request):
    ''' for storing each user's suscription for their chosen countries for stat updates '''
    
    global selected_country_for_updates
    global email
    global update_mails
    if request.method == "POST":
        email_id = request.POST["user_email"]
        
        if email_id == "":
            email_id = request.user.email
            email = request.user.email

        country = request.POST["selectedCountry"]
        selected_country_for_updates = country.capitalize()
        
        subscribed_countries = update_mails.get(email_id,[])
        if country.capitalize() not in subscribed_countries:
            subscribed_countries.append(country.capitalize())

        update_mails[email_id] = subscribed_countries
        
        message = f"You have subscribed for updates for {country} country."
        send_mail("Updates from Covid-Tracker",
                    message,
                    settings.EMAIL_HOST_USER,
                    [email_id],
                    fail_silently = False)
        print("EMAIL SENT")

    return render(request,"subscribe_success.html")