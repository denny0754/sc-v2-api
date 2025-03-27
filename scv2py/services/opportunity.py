from scv2py.services.base import SCV2BaseEndpoint

class OpportunityServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Opportunity Service.
    """
    OPPORTUNITY = 'opportunities'

    CATEGORY = 'categories'

    CONTACT_PARTY_ROLE = 'contactPartyRoles'

    CUSTOM_STATUS = 'customStatus'

    DOCUMENT_TYPE = 'documentTypes'

    FORECAST_CATEGORY = 'forecastCategories'

    LIFECYCLE_STATUS = 'lifeCycleStatus'

    PRIORITY = 'priorities'

    REASON_FOR_STATUS = 'reasonForStatus'

    SALES_CYCLE = 'salesCycles'

    SALES_PHASE = 'salesPhases'

    SALES_PHASE_PROGRESS = 'phaseProgress'

    SOURCE = 'sources'