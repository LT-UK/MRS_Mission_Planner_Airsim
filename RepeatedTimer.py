# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ========================================================= #
# Repeated Timer that can run in a separate thread
# To run this timer smoothly, ".join()" command in UAV operations should be avoided
# Usage Example
# rt = RepeatedTimer(1, AirsimIO.plotAllUAVsPaths, init.client, init.uavs, duration=1.1)
# rt.start()
# ...
# rt.stop()
# ========================================================= #

from threading import Timer

class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        # self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False