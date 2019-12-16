from flask import Flask, render_template, request, session, redirect
import sys
from random import shuffle

app = Flask(__name__)

##secret key needed to create session to store data for decision exercise.
##session approach recommended by former CS50 TA Sam Marullo
app.config['SECRET_KEY'] = 'secret key'

##Initial page to get user input
@app.route("/")
def input():
        return render_template("input.html")

##Implementing topological sort choice exercise - we begin by bringing the user form inputs into an array
##Exercise will consist of traversing across array in steps of 2, choosing "picks" that will go on to the next stage of selection
@app.route("/choice")
def choice():
    ##creating an array of user inputs
    choices=[]
    choices.extend(request.args.getlist("choice"))
    choices = list(filter(len, choices))
    if not choices:
        return render_template("error.html")
    shuffle(choices)
    ##setting up the session, including setting up a "picks" array and an index counter for traversing
    session["choices"]=choices
    session["picks"]=[]
    session["index"]=0
    return render_template("choose.html", choices=choices,index=0)

##Implementing our loop - as we traverse through the array, we make "picks" and update the various markers
@app.route("/choose")
def choose():
    choices=session["choices"]
    picks=session["picks"]
    index=session["index"]
    yourpick=int(request.args.get("yourpick"))
    picks.append(choices[yourpick])
    index += 2
    ##going through the initial array
    if (index < len(choices)-1):
        session["picks"]=picks
        session["index"]=index
    ##if we have an odd number of elements in the array, non-paired elements are automatically "pushed" into "picks" - we only care about our final, top choice
    elif (index == len(choices)-1):
        picks.append(choices[-1])
        session["choices"]=picks
        session["picks"]=[]
        session["index"]=0
        choices=picks
        index=0
    ##once we have exhausted our initial array, we reset and continue the process with the "picks", which are now the "choices"
    ##we continue looping through this process until only 1 pick and 1 choice remains, indicating we've picked our top choice
    else:
        session["choices"]=picks
        session["picks"]=[]
        session["index"]=0
        choices=picks
        index=0
    if (len(picks)==1 and len(choices)==1):
        return render_template("result.html", picks=picks)
    return render_template("choose.html", choices=choices, index=index)

