import unittest
from unittest.mock import MagicMock
from aiojsonrpc.router import Router
from aiojsonrpc.exceptions import MethodNotFound

class TestRouter(unittest.TestCase):
    """Testing Router class methods"""
    def test_add_new_method(self):
        """Testing add method to Router"""
        Router.clear()
        
        def test_method():
            pass

        Router.method(test_method)

        request = MagicMock()
        request.method = 'test_method'

        returned_method = Router.dispatch(request)

        assert returned_method is test_method

    def test_dublicate_method(self):
        """Testing adding dublicate method"""
        Router.clear()

        def test_method():
            pass

        Router.method(test_method)
        
        with self.assertRaises(ValueError) as context:
            Router.method(test_method)
    
    def test_cleaning_router(self):
        """Test cleaning Router"""
        Router.clear()

        def test_method():
            pass

        Router.method(test_method)

        Router.clear()

        request = MagicMock()
        request.method = 'test_method'

        with self.assertRaises(MethodNotFound) as context:
            returned_method = Router.dispatch(request)

    def test_method_not_found(self):
        """Test not existing method"""
        Router.clear()

        request = MagicMock()
        request.method = 'test_method'

        with self.assertRaises(MethodNotFound) as context:
            returned_method = Router.dispatch(request)
        

if __name__ == '__main__':
    unittest.main()
