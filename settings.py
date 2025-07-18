from types import SimpleNamespace
from enum import Enum

MAX_SIGNAL_LEN = 5000
FREQUENCY = 500  # измерений в секунду

TYPES_OF_STEP = SimpleNamespace(
    candidates='candidates',
    signal='signal'
)

# ключи json
JSON_KEYS = SimpleNamespace(
    STEP_ID_IN_TRACK = 'step_id',
    STEP_CLASS_NAME = 'step_class',
    STEP_ARGS = 'step_args'
)