from bot_modules.sign_up_for_services.services_realisation.services_realisation import Services
from bot_modules.sign_up_for_services.services_realisation.services_abstraction import (
    ServicesAbstraction,
)

services_realisation = Services()
services_abs = ServicesAbstraction(services_realisation)
