"""
Service definitions for the SAP Sales/Service Cloud V2 API.
"""

from scv2py.services.base import SCV2Service, SCV2BaseEndpoint
from scv2py.services.sales_territory import SalesTerritoryServiceEndpoint
from scv2py.services.collections_integration import CollectionsIntegrationServiceEndpoint
from scv2py.services.contact_person import ContactPersonServiceEndpoint
from scv2py.services.organizational_unit import OrganizationalUnitServiceEndpoint

__all__ = [
    'SCV2Service',
    'SCV2BaseEndpoint',
    'SalesTerritoryServiceEndpoint',
    'CollectionsIntegrationServiceEndpoint',
    'ContactPersonServiceEndpoint',
    'OrganizationalUnitServiceEndpoint'
]