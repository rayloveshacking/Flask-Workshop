import json
import random
import atexit
from random import choices

from flask import Flask, redirect, url_for, request, render_template, make_response

app = Flask(__name__)

with open("database.json", "r") as file:
    db = json.load(file) #This is how the db got initialized from the json file.

def save_db():
    with open("database.json", "w") as file:
        file.write(json.dumps(db, indent=2)) 

atexit.register(save_db)

print(db["choices"][0]) #Print the first choice of the db in the terminal.

def get_random_choices():
    if not db:
        raise Exception("Database not initialized yet") #Returns error if there is no db.
    if len(db["choices"]) < 2: #If there are less than two choices in the db, then return this exception error.
        raise Exception("Please add more than 2 choices")
    choice1 = random.choice(db["choices"]) #Uses random to get a random choice from choices of db
    choice2 = random.choice(db["choices"]) #Same done here.
    while choice2 == choice1:
        choice2 = random.choice(db["choices"]) #If the choice 2 and choice 1 are the same then use random to get a new choice from the db.
    return choice1, choice2

def find_choice(choice_id: str): #take the choice id from the user posted request json.
    if not db:
        raise Exception("Database not initialized yet") #Return error if database is not found.
    for choice in db["choices"]: #Go through each choice in database choices
        print(choice) #Print each choice in the choices.
        if choice["id"] == choice_id: #If the choice from the choices from the database is same as the choice id
            return choice #Return this back from the function.
    else:
        return None

@app.route('/', methods=["GET", "POST"])  #When the / is used only with either GET or POST 
def home(): #Use this home definition
    ## TODO: POST scores
    if request.method == "GET":
        choices = get_random_choices() #Get the two random choices from the db.
        return render_template('index.html', choices=choices)  # Give the user back the index.html and pass in the choices from the db.
    if request.method == "POST":
        print(request.json)
        choice = find_choice(request.json["choice"]) #Find the correct choice  from the database
        if not choice:
            return "Invalid choice", 400 #Return error if there is no choice in the database.
        choice["votes"] += 1 #Update the found choice's votes
        save_db() #Update the json file and save the updated score.
        return "Success", 200 #Return 200.

@app.route('/leaderboard')
def leaderboard():
    choices = db["choices"] #Get all of the choices from the database.
    choices = sorted(choices, key=lambda x: x["votes"], reverse=True) #Sort the choices by their votes in descending order.
    return render_template('leaderboard.html', choices=choices) #Return leaderboard.html and pass choices in to it.


if __name__ == "__main__":
    app.run(debug=True)

