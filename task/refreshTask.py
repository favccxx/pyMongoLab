from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

def tick():
    print('Tick! The time is: %s' % datetime.now())