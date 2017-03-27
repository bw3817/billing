from billing.tests import *

class TestAddhoursController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='addhours', action='index'))
        # Test response...
