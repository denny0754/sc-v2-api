"""
Exceptions raised by the scv2_api package.
"""

from scv2_api.exceptions.api_exceptions import (
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