from nefertari.authentication.views import (
    TicketAuthRegisterView as NefTicketAuthRegisterView,
    TicketAuthLoginView as NefTicketAuthLoginView,
    TicketAuthLogoutView as NefTicketAuthLogoutView,
)

from example_api.models import User


""" Not implemented by default nefertari ticket auth views:

    * Check for user to be active on register
    * Making user 'status' being 'active' on register
    * Checking user 'status' is not 'blocked', 'inactive' on login
    * Calling user.on_login()
"""


class TicketAuthRegisterView(NefTicketAuthRegisterView):
    Model = User


class TicketAuthLoginView(NefTicketAuthLoginView):
    Model = User


class TicketAuthLogoutView(NefTicketAuthLogoutView):
    Model = User
