class BaseRPCError(Exception):
    pass

    def get_data(self):
        return {'code': self.code, 'message': self.message}


class MethodNotFound(BaseRPCError):
    code = -32601
    message = 'Method not found'


class InvalidRequest(BaseRPCError):
    code = -32600
    message = 'Invalid Request'
    

class ParserError(BaseRPCError):
    code = -32700
    message = 'Parse error'


class InvalidParams(BaseRPCError):
    code = -32602
    message = 'Invalid method parameter(s)'


class InternalError(BaseRPCError):
    code = -32603
    message = 'Internal JSON-RPC error'
