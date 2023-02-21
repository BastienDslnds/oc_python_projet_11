def test_route_index(client):
    """Tester que l'url '/' est résolu vers la vue index."""

    response = client.get('/')
    print(response.__dict__)
    assert client.get('/').status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_clubs_remaining_points_displayed(client):
    """Tester que l'url '/board' est résolu vers la vue board."""

    response = client.get('/board')
    assert b"<td align=\'center\'>club one</td>" in response.data
    assert b"<td align=\'center\'>4</td>" in response.data


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


def test_event_places_available(client):
    """Le nombre d'inscriptions disponibles pour l'évènement
    doit être visible."""

    competition = 'first event'
    club = 'club one'
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200
    assert b'Places available: 20' in response.data


def test_message_booking_confirmation(client):
    """Si la réservation est confirmée alors:
    - la welcome page est affichée
    - un message de confirmation est obtenu"""

    competition = 'first event'
    club = 'club one'
    response = client.post(
        'purchasePlaces',
        data={'places': 2, 'competition': competition, 'club': club},
    )
    assert b'Great-booking complete! You booked 2 places' in response.data


def test_available_points_are_updated(client):
    """Tester que les points disponibles sont mis à jour
    après une réservation."""

    competition = 'first event'
    club = 'club two'
    response = client.post(
        '/purchasePlaces',
        data={'places': 10, 'club': club, 'competition': competition},
    )
    assert b'Points available: 5' in response.data


def test_available_places_are_updated(client):
    """Tester que les places disponibles sont mis à jour
    après une réservation."""

    competition = 'first event'
    club = 'club two'
    response = client.post(
        '/purchasePlaces',
        data={'places': 1, 'club': club, 'competition': competition},
    )
    assert b'Number of Places: 19' in response.data


def test_should_not_be_able_to_use_more_than_available_points(client):
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


def test_should_not_be_able_to_use_more_than_max_allowed_places(client):
    """Si le nombre de places demandées est supérieur à 12 alors:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    competition = 'second event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 13, 'club': club, 'competition': competition},
    )
    assert b"You are not able to book more than 12 places." in response.data


def test_should_not_be_able_to_use_more_than_available_places(client):
    """Si le nombre de places demandées est supérieur aux places disponibles alors:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

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


def test_should_not_be_able_to_book_full_event(client):
    """Si le concours est complet:
    - la vue de booking est ré-affichée
    - un message d'erreur spécifique est affiché"""

    competition = 'third event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 11, 'club': club, 'competition': competition},
    )
    assert b"The event is already full." in response.data


def test_should_not_book_past_competition(client):
    """Créer une compétition avec une date inférieure à la date d'aujourd'hui."""

    competition = 'fourth event'
    club = 'club two'
    response = client.post(
        'purchasePlaces',
        data={'places': 11, 'club': club, 'competition': competition},
    )
    assert (
        b"You are not able to book places in past competition."
        in response.data
    )


def test_book_unknown_club(client):
    competition = 'first event'
    club = 'club three'
    response = client.get(f'/book/{competition}/{club}')
    assert b'Something went wrong-please try again' in response.data


def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
