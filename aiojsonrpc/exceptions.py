class BaseJSONRPCException(Exception):
    pass

class MethodNotFound(BaseJSONRPCException):
    code = -32601
    message = 'Method not found'

    def get_data(self):
        return {'code': self.code, 'message': self.message}


class InvalidRequest(BaseJSONRPCException):
    code = -32600
    message = 'Invalid Request'

    def get_data(self):
        return {'code': self.code, 'message': self.message}
    
class ParserError(BaseJSONRPCException):
    code = -32700
    message = 'Parse error'

    def get_data(self):
        return {'code': self.code, 'message': self.message}