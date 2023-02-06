import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs(file):
    with open(file) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions(file):
    with open(file) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='something_special')

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if test_config is None:
        clubs = loadClubs('clubs.json')
        competitions = loadCompetitions('competitions.json')
    else:
        app.config.from_mapping(test_config)
        clubs = loadClubs('tests/clubs_test.json')
        competitions = loadCompetitions('tests/competitions_test.json')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        club = [
            club for club in clubs if club['email'] == request.form['email']
        ]
        if club:
            club = club[0]
            return render_template(
                'welcome.html', club=club, competitions=competitions
            )
        else:
            error_message = "Sorry, that email was not found."
            return render_template('index.html', message=error_message)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [
            c for c in competitions if c['name'] == competition
        ][0]
        if foundClub and foundCompetition:
            return render_template(
                'booking.html', club=foundClub, competition=foundCompetition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                'welcome.html', club=club, competitions=competitions
            )

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [
            c for c in competitions if c['name'] == request.form['competition']
        ][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = (
            int(competition['numberOfPlaces']) - placesRequired
        )
        flash('Great-booking complete!')
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
