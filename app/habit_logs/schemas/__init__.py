from .create_habit_log_schema import CreateHabitLogSchema
from .habit_log_schema import HabitLogSchema
from .habit_logs_response_schema import HabitLogsResponseSchema

# Preserve the name used by the existing router.
HabitLogsResponse = HabitLogsResponseSchema
