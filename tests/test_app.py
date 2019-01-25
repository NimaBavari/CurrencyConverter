import os, sys, unittest

from flask_testing import TestCase

sys.path.append(os.path.abspath('..'))

from app import app


class TestApp(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def is_page_successful(self):
        with self.client:
            self.assertEqual(self.client.get('/').status_code, 200)


if __name__ == '__main__':
    unittest.main()

