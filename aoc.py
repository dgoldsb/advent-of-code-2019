import os
import requests
from typing import List


with open("session_cookie") as f:
    session = f.readline().strip()

os.environ["AOC_SESSION"] = session

