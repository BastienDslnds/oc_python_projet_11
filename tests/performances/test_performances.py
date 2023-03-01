from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def showSummary(self):
        """Connexion avec un email
        pour obtenir la page welcome.html
        avec la liste des compétitions."""

        email = 'john@simplylift.co'
        self.client.post('/showSummary', data={'email': email})

    @task
    def purchasePlaces(self):
        """Acheter des places pour un évènement.
        Retour sur la page welcome.html après l'achat."""

        competition = 'Spring Festival'
        club = 'Simply Lift'
        self.client.post(
            '/purchasePlaces',
            data={'places': 2, 'competition': competition, 'club': club},
        )
