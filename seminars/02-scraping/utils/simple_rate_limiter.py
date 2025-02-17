import time
import threading

class SimpleRateLimiter:
    def __init__(self, rate):
        self._lock = threading.Lock()
        self._delta = 1. / rate
        self._last_called_ts = 0

    def get_delay(self, now=None):
        with self._lock:
            if now is None:
                now = time.time()
            expected_next_call_ts = max(self._last_called_ts + self._delta, now)
            self._last_called_ts = expected_next_call_ts
            return max(expected_next_call_ts - now, 0)