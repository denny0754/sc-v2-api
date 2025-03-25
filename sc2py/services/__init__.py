"""
Service definitions for the SAP Sales/Service Cloud V2 API.
"""

from sc2py.services.base import SCV2Service, SCV2BaseEndpoint
from sc2py.services.sales_territory import SalesTerritoryServiceEndpoint
from sc2py.services.collections import CollectionsIntegrationServiceEndpoint
from sc2py.services.contact_person import ContactPersonServiceEndpoint
from sc2py.services.organizational import OrganizationalUnitServiceEndpoint

__all__ = [
    'SCV2Service',
    'SCV2BaseEndpoint',
    'SalesTerritoryServiceEndpoint',
    'CollectionsIntegrationServiceEndpoint',
    'ContactPersonServiceEndpoint',
    'OrganizationalUnitServiceEndpoint'
]