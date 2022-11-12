from bot_modules.schedule.schedule_realisation.schedule_abstraction import (
    ScheduleAbstraction,
)
from bot_modules.schedule.schedule_realisation.schedule_realsiation import (
    ScheduleRealisation,
)


schedule_realisation = ScheduleRealisation()
schedule_abs = ScheduleAbstraction(schedule_realisation)
