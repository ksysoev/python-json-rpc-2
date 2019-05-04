import json
import unittest
from aiojsonrpc.router import Router
from aiojsonrpc import Server, BaseRPCError

class TestErrors(unittest.TestCase):
    """Testing Router class methods"""
    def test_with_invalid_request(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": 1, "params": "bar"}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}')

    
    def test_with_invalid_json(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": 1, "params": "ba')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": null}')

    def test_with_method_not_found(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "test_method", "params": [1, 2 ,3], "id": 1}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 1}')

    def test_with_invalid_params(self):
        Router.clear()
        
        test_server = Server()

        def subtract(minuend, subtrahend):
            return minuend - subtrahend
        Router.method(subtract)

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "subtract", "params": [1, 2 ,3], "id": 1}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid method parameter(s)"}, "id": 1}')

    def test_with_internal_server_error(self):
        Router.clear()
        
        test_server = Server()

        def test_method():
            raise Exception('Some Error')
        Router.method(test_method)

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "test_method", "id": 1}')
        
        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32603, "message": "Internal JSON-RPC error"}, "id": 1}')

    def test_with_custom_error(self):
        Router.clear()
        
        test_server = Server()

        class CustomError(BaseRPCError):
            code = 42
            message = 'Custom error'

            
        def test_method():
            raise CustomError()

        Router.method(test_method)

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "test_method", "id": 1}')
        
        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": 42, "message": "Custom error"}, "id": 1}')

if __name__ == '__main__':
    unittest.main()
