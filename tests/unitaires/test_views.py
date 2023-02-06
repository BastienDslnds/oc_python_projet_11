def test_route_index(client):
    """Tester que l'url de la vue index est bien obtenu."""
    response = client.get('/')
    assert response.headers["Location"] == "/"
    assert client.get('/').status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_clubs_remaining_points_displayed(client):
    """Un tableau des points disponibles pour chaque club
    doit être accessible sans se connecter au site."""
    pass


def test_login_with_correct_email(auth):
    """Si l'email est connu alors
    je suis redirigé vers la page welcome.html."""

    response = auth.login()
    assert response.status_code == 200
    assert b'Welcome, club_one@test.com ' in response.data


def test_login_with_incorrect_email(auth):
    """Si l'email est inconnu alors:
    - la vue de l'index est ré-affichée
    - un message d'erreur est affiché."""

    response = auth.login('test_incorrect@test.com')
    assert response.status_code == 200
    assert b"Sorry, that email was not found." in response.data


def test_event_places_available(auth, client):
    """Le nombre d'inscriptions disponibles pour l'évènement doit être visible."""
    # response = auth.login()
    competition = 'first event'
    club = 'club one'
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200
    assert b'Places available: 20' in response.data


def test_message_booking_confirmation(auth, client):
    """Si la réservation est confirmée alors:
    - la welcome page est affichée
    - un message de confirmation est obtenu"""
    response = auth.login()
    competition = 'first event'
    club = 'club one'
    response = client.post(
        'purchasePlaces',
        data={'places': 5, 'competition': competition, 'club': club},
    )
    assert b'Great-booking complete!' in response.data


def test_available_points_are_updated(auth, client):
    """Tester que les points disponibles sont mis à jour
    après une réservation."""

    auth.login('club_two@test.com')
    competition = 'first event'
    club = 'club two'
    response = client.post(
        '/purchasePlaces',
        data={'places': 10, 'club': club, 'competition': competition},
    )
    print(response.data)
    assert b'Points available: 5' in response.data


def test_should_not_be_able_to_use_more_than_available_points(auth, client):
    """Si le nombre de places demandées est supérieur aux points disponibles:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    competition = 'first event'
    club = 'club one'
    response = client.post(
        'purchasePlaces',
        data={'places': 5, 'competition': competition, 'club': club},
    )
    assert (
        b"You are not able to use more than your available points."
        in response.data
    )


def test_should_not_be_able_to_use_more_than_max_allowed_places(auth, client):
    """Si le nombre de places demandées est supérieur à 12 alors:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    auth.login('club_two@test.com')
    competition = 'second event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 13, 'club': club, 'competition': competition},
    )
    assert b"You are not able to book more than 12 places." in response.data


def test_should_not_be_able_to_use_more_than_available_places(auth, client):
    """Si le nombre de places demandées est supérieur aux places disponibles alors:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    auth.login('club_two@test.com')
    competition = 'second event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 11, 'club': club, 'competition': competition},
    )
    assert (
        b"You are not able to book more than available places."
        in response.data
    )


def test_should_not_be_able_to_book_full_event(auth, client):
    """Si le concours est complet:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    # auth.login('club_two@test.com')
    competition = 'third event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 11, 'club': club, 'competition': competition},
    )
    assert b"The event is already full." in response.data


def test_should_not_book_past_competition(auth, client):
    """Créer une compétition avec une date inférieure à la date d'aujourd'hui."""

    # auth.login('club_two@test.com')
    competition = 'third event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 11, 'club': club, 'competition': competition},
    )
    assert (
        b"You are not able to book places in past competition."
        in response.data
    )
