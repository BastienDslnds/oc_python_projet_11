from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    # S'assurer que le temps de chargement ne dépasse jamais 5 secondes
    def getCompetitionsList(self):
        """Connexion avec un email
        pour obtenir la page welcome.html
        avec la liste des compétitions."""

        email = 'club_one@test.com'
        self.client.post('/showSummary', data={'email': email})

    @task
    # S'assurer que les mises à jour ne prennent pas plus de 2 secondes
    def updateTotalPoints(self):
        """Acheter des places pour un évènement.
        Retour sur la page welcome.html après l'achat."""

        competition = 'first event'
        club = 'club one'
        self.client.post(
            '/purchasePlaces',
            data={'places': 2, 'competition': competition, 'club': club},
        )
