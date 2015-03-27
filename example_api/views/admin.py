import logging
from pyramid.security import *

from nefertari.utility_views import LogLevelView, SettingsView as PSettigsView

import example_api
log = logging.getLogger(__name__)

hide = [
    '-auth_tkt_secret',
    '-system.user',
    '-system.email',
    '-system.password',
]

class SettingsView(PSettigsView):
    settings = example_api.Settings.subset(hide)

log = logging.getLogger(__name__)
