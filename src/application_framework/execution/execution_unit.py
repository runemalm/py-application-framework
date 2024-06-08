from enum import Enum

class ExecutionUnit(Enum):
    Process = "process"
    Thread = "thread"
    Coroutine = "coroutine"
