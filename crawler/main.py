import requests
import time
from twisted.internet import task, reactor

STUDIO_ID = 1217120190
X_TENANT = "speedfitness"


def append_line(s):
    with open("data.csv", "a") as myfile:
        myfile.write(f"{s}\n")


def crawl_and_store():
    try:
        res = requests.get(f"https://www.mysports.com/nox/public/v1/studios/{STUDIO_ID}/utilization/v2/today",
                           headers={"x-tenant": X_TENANT})
        current_time_entry = next(filter(lambda time_entry: time_entry["current"], res.json()), None)
        percentage = current_time_entry["percentage"]
        append_line(f"{int(time.time())},{percentage}")
    except Exception:
        pass


loopingCall = task.LoopingCall(crawl_and_store)
loopingCall.start(60)
reactor.run()
