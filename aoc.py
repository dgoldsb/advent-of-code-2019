import os
import requests
from typing import List


def get_input(day: int, year: int = 2019) -> List[str]:
    filename = f"input/{str(day)}.txt"
    
    if not os.path.exists(filename):
        with open("session_cookie") as f:
            session = f.readline().strip()
        req = requests.get(f"https://adventofcode.com/{str(year)}/day/{str(day)}/input", cookies={"session": session})
        req.raise_for_status()
        with open(filename, "wb") as f:
            f.write(req.content)
    
    with open(filename, "r") as f:
        return [x.rstrip("\n") for x in f.readlines()]

