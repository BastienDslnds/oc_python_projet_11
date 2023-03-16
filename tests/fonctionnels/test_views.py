from flask import Flask
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestAuthentification(LiveServerTestCase):
    def create_app(self):
        """Lancement de l'application avec une configuration de test."""

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Etapes communes à chaque test:
        - Lancement de l'application
        - Création d'un client HTTP à l'aide d'un webdriver
        - Ouvrir une page chrome sur le localhost."""

        self.browser = webdriver.Chrome("tests/fonctionnels/chromedriver")
        self.browser.get(self.get_server_url())

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        """Tester la connexion."""

        email = self.browser.find_element(By.NAME, "email")
        email.send_keys('club_one@test.com')

        enter = self.browser.find_element(By.TAG_NAME, 'button')
        enter.click()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + '/showSummary'
        )


# def test_login_with_incorrect_email(self):
#     """Tester la connexion avec un email incorrect."""

#     email = self.browser.find_element(By.NAME, "email")
#     email.send_keys('incorrect@test.com')

#     enter = self.browser.find_element(By.TAG_NAME, 'button')
#     enter.click()

#     self.assertEqual(
#         self.browser.page_source.find('Sorry, that email was not found.'),
#         -1,
#     )
#     self.assertEqual(self.browser.current_url, self.live_server_url + '/')


# class TestBooking(LiveServerTestCase):
#     def create_app(self):
#         app = Flask(__name__)
#         app.config['TESTING'] = True
#         return app

#     def setUp(self):
#         self.app = self.create_app()
#         self.browser = webdriver.Chrome("tests/performances/chromedriver")
#         self.browser.get(self.live_server_url)

#     def signin(self):
#         email = self.browser.find_element(By.NAME, "email")
#         email.send_keys('club_one@test.com')

#         enter_button = self.browser.find_element(By.TAG_NAME, 'button')
#         enter_button.click()

#     def bookEvent(self):
#         # competition = 'first event'
#         # club = 'club one'
#         # url = f'/book/{competition}/{club}'
#         book = self.browser.find_elements(By.LINK_TEXT, 'Book Places')[1]
#         # book = self.browser.find_element(By.XPATH, "html/body/ul/li[1]/a]")
#         book.click()

#     def tearDown(self):
#         self.browser.quit()

#     def test_message_booking_confirmation(self):
#         self.signin()
#         self.bookEvent()

#         places = self.browser.find_element(By.TAG_NAME, 'places')
#         places.send_keys("2")

#         book_button = self.browser.find_element(By.TAG_NAME, 'button')
#         book_button.click()

#         self.assertEqual(
#             self.browser.current_url, self.live_server_url + '/showSummary'
#         )
#         self.assertEqual(
#             self.browser.page_source.find(
#                 'Great-booking complete! You booked 2 places'
#             ),
#             1,
#         )
#         # self.assertIn()

#     def test_should_not_be_able_to_use_more_than_available_points(self):
#         self.signin()
#         self.bookEvent()
#         pass
