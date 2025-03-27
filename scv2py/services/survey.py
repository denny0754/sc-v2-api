from scv2py.services.base import SCV2BaseEndpoint

class SurveyServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Account Service.
    """

    DESIGNS : dict = {
        'GET': 'designs',
        'POST': 'designs'
    }

    DESIGN : dict = {
        'GET': 'designs/{id}',
        'DELETE': 'designs/{id}'
    }

    DESIGN_ELEMENT : dict = {
        'POST': 'designs/{id}/elements',
        'PATCH': 'designs/{id}/elements/{elementId}',
        'DELETE': 'designs/{id}/elements/{elementId}'
    }

    DESIGN_PRODUCT : dict = {
        'POST': 'designs/{id}/products',
        'DELETE': 'designs/{id}/products/{productId}'
    }