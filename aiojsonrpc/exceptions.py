"""JSON RPC Errors

Package contains predefined errors
"""

from abc import ABCMeta

class BaseRPCError(Exception, metaclass=ABCMeta):
    """Base class for JSON RPC Errors"""

    code = None
    message = None

    def get_data(self):
        """Method returns data for error response"""

        return {'code': self.code, 'message': self.message}


class MethodNotFound(BaseRPCError):
    """The class for exceptions that are raised for situation when requered method isn't found"""

    code = -32601
    message = 'Method not found'


class InvalidRequest(BaseRPCError):
    """The class for exceptions that are raised for situation when request has invalid format"""

    code = -32600
    message = 'Invalid Request'


class ParserError(BaseRPCError):
    """The class for exceptions that are raised for situation when request contains invalid json"""

    code = -32700
    message = 'Parse error'


class InvalidParams(BaseRPCError):
    """The class for exceptions that are raised for situation
    when request contains invalid parameters
    """

    code = -32602
    message = 'Invalid method parameter(s)'


class InternalError(BaseRPCError):
    """The class for exceptions that are raised for situation
    when in proccessing request was catched exception
    """

    code = -32603
    message = 'Internal JSON-RPC error'
