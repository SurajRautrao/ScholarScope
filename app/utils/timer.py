import time

class Timer:
    def __init__(self):
        self.times = {}

    def start(self, name):
        self.times[name] = {"start": time.time(), "duration": None}

    def stop(self, name):
        if name in self.times and self.times[name]["start"]:
            self.times[name]["duration"] = time.time() - self.times[name]["start"]

    def get(self, name):
        return self.times.get(name, {}).get("duration", 0)

    def get_all(self):
        return {k: v["duration"] for k, v in self.times.items()}
