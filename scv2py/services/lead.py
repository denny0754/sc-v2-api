from scv2py.services.base import SCV2BaseEndpoint

class LeadServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Lead Service.
    """
    LEAD = 'leads'

    QUALIFICATION = 'qualifications'

    REASON_FOR_STATUS = 'reasonForStatus'

    SOURCE = 'sources'

    STATUS = 'statuses'