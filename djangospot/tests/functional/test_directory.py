from djangospot.tests import *

class TestDirectoryController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='directory', action='index'))
        # Test response...
