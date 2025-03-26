from sc2py.services.base import SCV2BaseEndpoint

class CollectionsIntegrationServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Collections Integration Service.
    """
    CORRESPONDENCE_HISTORY = 'correspondenceHistory'
    DUNNING = 'dunning'
    RETURNS = 'returns'
    WRITE_OFF = 'writeOff'