from enum import Enum


class ExecutionMode(Enum):
    MAIN_EVENT_LOOP_ASYNC = 'main_event_loop_async'
    SEPARATE_THREAD = 'separate_thread'
    SEPARATE_THREAD_ASYNC = 'separate_thread_async'
    SEPARATE_PROCESS = 'separate_process'
    SEPARATE_PROCESS_ASYNC = 'separate_process_async'
