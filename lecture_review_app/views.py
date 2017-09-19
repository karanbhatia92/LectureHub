# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

import datetime
import databaseconnection
import sentiment_analysis
import ast

engine = databaseconnection.initialize()



# Create your views here.
def login(request):
    request.session["user_name"] = ""
    request.session["user_type"] = ""
    request.session["lec_id_ele"] = "021"
    if "user_name" in request.session and "user_type" in request.session:
            if(request.session["user_type"] == 0):
                return redirect(notes)
            if(request.session["user_type"] == 1):
                return redirect(dashboard)

    if request.method == "POST":
        input_email = request.POST.get("inputEmail", None)
        input_password = request.POST.get("inputPassword", None)

        if input_email != "" and input_password != "":
            user_type = databaseconnection.login(engine, input_email, input_password)
            # return render(request, "hello.html", {"input_email": input_email, "input_password": input_password, "user_type": user_type})

            if(user_type != None):
                request.session["user_type"] = user_type
                request.session["user_name"] = input_email
                if(user_type == 0):
                    return redirect(notes)
                if(user_type == 1):
                    return redirect(dashboard)
    return render(request, "login.html", {})

def logout(request):
    if "user_name" in request.session:
        del request.session["user_name"]
    if "user_type" in request.session:
        del request.session["user_type"]
    return redirect(login)

def notes(request):

    if not check_loggedin(request):
        return redirect(login)

    if(request.session["user_type"] != 0):
        return redirect(login)

    lec_id = ""
    json_string = ""
    lecs = databaseconnection.get_lectures(engine)

    if request.method == "POST":
        user_name = request.session["user_name"]
        if "lec_id_ele_submit" in request.POST:
            request.session["lec_id_ele"] = (request.POST.get("lec_id_ele", None))
            lec_id = request.session["lec_id_ele"]
            json_string = databaseconnection.get_notes(engine, user_name, lec_id)
        else:
            json_string = request.POST.get("name_notes", None)
            lec_id = request.session["lec_id_ele"]
            databaseconnection.add_notes(engine, user_name, lec_id, json_string)

    return render(request, "notes.html", {"sess_user_type":request.session["user_type"], "sess_lec_id": request.session["lec_id_ele"], "lecs": lecs, "lec_id": lec_id, "json_string": json_string})

def rating(request):

    if not check_loggedin(request):
        return redirect(login)

    if(request.session["user_type"] != 0):
        return redirect(login)

    lecs = databaseconnection.get_lectures(engine)

    if request.method == "POST":
        if "lec_id_ele_submit" in request.POST:
            request.session["lec_id_ele"] = (request.POST.get("lec_id_ele", None))
        elif "rating_submit" in request.POST:
            lecture_id = request.session["lec_id_ele"]
            rating = int(request.POST.get("inputWalls", None))
            comment = str(request.POST.get("message-text", None))
            sentiment_value = sentiment_analysis.analyzesentiment(comment)
            databaseconnection.submit_comment(engine, lecture_id, comment, rating, sentiment_value, request.session["user_name"])
    return render(request, "rating.html", {"sess_user_type":request.session["user_type"], "sess_lec_id": request.session["lec_id_ele"], "lecs": lecs})

def dashboard(request):
    if not check_loggedin(request):
        return redirect(login)

    lecs = databaseconnection.get_lectures(engine)

    if request.method == "POST":
        if "lec_id_ele_submit" in request.POST:
            request.session["lec_id_ele"] = (request.POST.get("lec_id_ele", None))

    data1 =  databaseconnection.retrieve_sentiment_students(engine, request.session["lec_id_ele"])
    data2 =  databaseconnection.retrieve_rating_students(engine, request.session["lec_id_ele"])

    from graphos.sources.simple import SimpleDataSource
    from graphos.renderers.yui import LineChart
    from graphos.renderers.yui import PieChart

    chart1 = LineChart(SimpleDataSource(data=data1))
    chart2 = PieChart(SimpleDataSource(data=data2))

    return render(request, "dashboard.html", {"sess_user_type":request.session["user_type"], "chart1": chart1, "chart2": chart2, "sess_lec_id": request.session["lec_id_ele"], "lecs": lecs})

def comment_dashboard(request):
    if not check_loggedin(request):
        return redirect(login)
    lecs = databaseconnection.get_lectures(engine)

    if request.method == "POST":
        if "lec_id_ele_submit" in request.POST:
            request.session["lec_id_ele"] = (request.POST.get("lec_id_ele", None))

    data =  databaseconnection.retrieve_catergories(engine, request.session["lec_id_ele"])

    return render(request, "comment_dashboard.html", {"sess_user_type":request.session["user_type"], "sess_lec_id": request.session["lec_id_ele"], "lecs": lecs, "one": data["one"], "two": data["two"], "three": data["three"], "four": data["four"], "five": data["five"]})

def course_dashboard(request):
    if not check_loggedin(request):
        return redirect(login)

    lecs = databaseconnection.get_lectures(engine)

    if request.method == "POST":
        if "lec_id_ele_submit" in request.POST:
            request.session["lec_id_ele"] = (request.POST.get("lec_id_ele", None))

    data1 =  databaseconnection.retrieve_lecture_sentiment(engine, 0)
    data2 =  databaseconnection.retrieve_lecture_rating(engine, 0)

    from graphos.sources.simple import SimpleDataSource
    from graphos.renderers.yui import LineChart

    chart1 = LineChart(SimpleDataSource(data=data1))
    chart2 = LineChart(SimpleDataSource(data=data2))

    return render(request, "course_dashboard.html", {"sess_user_type":request.session["user_type"], "chart1": chart1, "chart2": chart2, "sess_lec_id": request.session["lec_id_ele"], "lecs": lecs})

def generate_lecture_id(request):
    if not check_loggedin(request):
        return redirect(login)

    if(request.session["user_type"] != 1):
        return redirect(login)

    lecture_id = 0

    if request.method == "POST":
        if "submit_gen_lecture_id" in request.POST:
            course_name = str(request.POST.get("exampleSelect1", None))
            lecture_name = str(request.POST.get("exampleTextarea", None))
            lecture_id = databaseconnection.add_lecture(engine, course_name, lecture_name)
    return render(request, "generate_lecture_id.html", {"sess_user_type":request.session["user_type"], "lecture_id": lecture_id})



def check_loggedin(request):
    if "user_name" in request.session and "user_type" in request.session:
        return True
    return False
