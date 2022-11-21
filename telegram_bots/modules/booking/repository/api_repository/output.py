from telegram_bots.modules.booking.repository.api_repository.realisation import BookingRepositoryRealisationDatabase
from telegram_bots.modules.booking.repository.api_repository.abstraction import BookingRepositoryAbstraction


booking_repository_realisation_database = BookingRepositoryRealisationDatabase()
booking_repository_abstraction = BookingRepositoryAbstraction(booking_repository_realisation_database)
