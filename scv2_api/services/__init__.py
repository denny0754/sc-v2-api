"""
Service definitions for the SAP Sales/Service Cloud V2 API.
"""

from scv2_api.services.base import SCV2Service, SCV2BaseEndpoint
from scv2_api.services.sales_territory import SalesTerritoryServiceEndpoint
from scv2_api.services.collections import CollectionsIntegrationServiceEndpoint
from scv2_api.services.contact_person import ContactPersonServiceEndpoint
from scv2_api.services.organizational import OrganizationalUnitServiceEndpoint

__all__ = [
    'SCV2Service',
    'SCV2BaseEndpoint',
    'SalesTerritoryServiceEndpoint',
    'CollectionsIntegrationServiceEndpoint',
    'ContactPersonServiceEndpoint',
    'OrganizationalUnitServiceEndpoint'
]