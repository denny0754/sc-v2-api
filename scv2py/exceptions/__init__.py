"""
Exceptions raised by the scv2_api package.
"""

from sc2py.exceptions.api_exceptions import (
    SCV2InvalidEndpointException,
    SCV2ConnectionError,
    SCV2RequestError,
    SCV2TimeoutError
)

__all__ = [
    'SCV2InvalidEndpointException',
    'SCV2ConnectionError',
    'SCV2RequestError',
    'SCV2TimeoutError'
]