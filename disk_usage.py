#!/usr/bin/env python

import requests
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.environ["URL"]
LOG = os.environ["LOG"]

usage = subprocess.check_output(["df", "/"]).decode("ASCII")
usage = usage.splitlines()[1].split()
percent = usage[4]
used = int(usage[2])
full = int(usage[1])
text = f"Disk usage: {percent}"

try:
    prev = subprocess.check_output(["tail", "-n1", LOG]).decode("ASCII")
except:
    prev_time = 0
    prev_used = 0
else:
    prev = prev.split("\t")
    prev_time = int(prev[1])
    prev_used = int(prev[3])

now = datetime.now()
human = now.strftime("%Y-%m-%d %H:%M:%S")
seconds = int(now.timestamp())

dy = used - prev_used
dx = seconds - prev_time
if dy > 0:
    estimate = dx * (full - used) / dy
    text += f"\nIncresed {dy // 1024} MB in {dx // 60} minutes. Estimated disk full: {estimate // 60 // 60 // 24} days"


fo = open(LOG, "a")
fo.write(f"{human}\t{seconds}\t{percent}\t{used}\n")
fo.close()

print(text)

data = {"text": text}
response = requests.post(
    URL,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)
