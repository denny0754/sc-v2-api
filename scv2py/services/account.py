from scv2py.services.base import SCV2BaseEndpoint

class AccountServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Account Service.
    """
    ACCOUNTS : dict = {
        'GET': 'accounts',
        'POST': 'accounts'
    }

    ACCOUNT : dict = {
        'GET': 'accounts/{id}',
        'PATCH': 'accounts/{id}'
    }