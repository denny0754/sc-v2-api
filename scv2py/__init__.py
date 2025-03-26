"""
SAP Sales/Service Cloud V2 API Wrapper

A Python library for interacting with the SAP Sales/Service Cloud V2 API.
"""

__version__ = '0.1.0'

# Import public API classes
from scv2py.core.session import SCV2Session
from scv2py.core.request import SCV2Request, SCV2RequestBuilder, SCV2RequestType
from scv2py.core.batch import SCV2ClientBatchRequest

# Import service definitions
from scv2py.services import (
    SCV2Service,
    SalesTerritoryServiceEndpoint,
    CollectionsIntegrationServiceEndpoint,
    ContactPersonServiceEndpoint,
    OrganizationalUnitServiceEndpoint
)

# Import exceptions
from scv2py.exceptions import (
    SCV2InvalidEndpointException,
    SCV2ConnectionError,
    SCV2RequestError,
    SCV2TimeoutError
)

# Define what's available with wildcard imports
__all__ = [
    'SCV2Session',
    'SCV2Request',
    'SCV2RequestBuilder',
    'SCV2RequestType',
    'SCV2ClientBatchRequest',
    'ODataQueryParameter',
    'SCV2Service',
    'SalesTerritoryServiceEndpoint',
    'CollectionsIntegrationServiceEndpoint',
    'ContactPersonServiceEndpoint',
    'OrganizationalUnitServiceEndpoint',
    'SCV2InvalidEndpointException',
    'SCV2ConnectionError',
    'SCV2RequestError',
    'SCV2TimeoutError'
]