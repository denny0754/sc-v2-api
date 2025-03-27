from scv2py.services.base import SCV2BaseEndpoint

class AppointmentServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Account Hierarchy Service.
    """
    APPOINTMENT = 'appointments'

    APPOINTMENT_CATEGORY = 'categories'

    APPOINTMENT_PRIORITY = 'prorities'

    APPOINTMENT_STATUS = 'status'