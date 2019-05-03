import json
import unittest
from aiojsonrpc.router import Router
from aiojsonrpc import Server
import functools

class CallRPC(unittest.TestCase):
    def test_with_positional_parameters_1(self):
        Router.clear()
        
        def subtract(minuend, subtrahend):
            return minuend - subtrahend
        
        Router.method(subtract)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}')


        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "result": 19, "id": 1}')

    def test_with_positional_parameters_2(self):
        Router.clear()
        
        def subtract(minuend, subtrahend):
            return minuend - subtrahend
        
        Router.method(subtract)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "result": -19, "id": 2}')

    def test_with_named_parameters_1(self):
        Router.clear()
        
        def subtract(minuend, subtrahend):
            return minuend - subtrahend

        Router.method(subtract)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "result": 19, "id": 3}')

    def test_with_named_parameters_2(self):
        Router.clear()
        
        def subtract(minuend, subtrahend):
            return minuend - subtrahend

        Router.method(subtract)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "result": 19, "id": 4}')

    def test_notification_1(self):
        Router.clear()
        
        def update(a,b,c,d,e):
            return 123

        Router.method(update)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}')

        assert str(result) == ''

    def test_notification_2(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}')

        assert str(result) == ''

    def test_notification_3(self):
        Router.clear()
        
        def foobar():
            return 123

        Router.method(foobar)

        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "foobar"}')

        assert str(result) == ''

    def test_notification_4(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "foobar"}')

        assert str(result) == ''
    
    def test_non_existent_method(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": "foobar", "id": "1"}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "1"}'), str(result)

    def test_with_invalid_request_object_1(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": 1, "params": "bar"}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}')


    def test_with_invalid_request_object_2(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('{"jsonrpc": "2.0", "method": 1, "params": "bar"}')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}')

class CallBatchRPC(unittest.TestCase):

    def test_invalid_json(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('[{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},'
                                      '{"jsonrpc": "2.0", "method"]')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": null}')

    def test_with_an_empty_array(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('[]')

        assert json.loads(str(result)) == json.loads('{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}')

    def test_with_an_invalid_batch_not_empty(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('[1]')

        assert json.loads(str(result)) == json.loads('[{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}]')

    def test_with_invalid_batch(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('[1,2,3]')

        assert json.loads(str(result)) == json.loads('[{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null},'
                          '{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null},'
                          '{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}]')


    def test_batch(self):
        Router.clear()

        def sum(*items):
            def add(x,y): return x+y
            return functools.reduce(add, items)
        Router.method(sum)

        def subtract(minuend, subtrahend):
            return minuend - subtrahend
        Router.method(subtract)

        def get_data():
            return ["hello", 5]
        Router.method(get_data)
        
        test_server = Server()

        result = test_server.dispatch('[{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},'
                                      '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},'
                                      '{"jsonrpc": "2.0", "method": "subtract", "params": [42,23], "id": "2"},'
                                      '{"foo": "boo"},'
                                      '{"jsonrpc": "2.0", "method": "foo.get", "params": {"name": "myself"}, "id": "5"},'
                                      '{"jsonrpc": "2.0", "method": "get_data", "id": "9"}]')

        assert json.loads(str(result)) == json.loads('[{"jsonrpc": "2.0", "result": 7, "id": "1"},'
                                                     '{"jsonrpc": "2.0", "result": 19, "id": "2"},'
                                                     '{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null},'
                                                     '{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "5"},'
                                                     '{"jsonrpc": "2.0", "result": ["hello", 5], "id": "9"}]')

    
    def test_all_notifications(self):
        Router.clear()
        
        test_server = Server()

        result = test_server.dispatch('[{"jsonrpc": "2.0", "method": "notify_sum", "params": [1,2,4]},'
                                      '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]}]')

        assert str(result) == ''





if __name__ == '__main__':
    unittest.main()