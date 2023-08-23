import os
import pathlib

from deez.contrib.serialization import json_loads

root = pathlib.Path(__file__).parent

with open(os.path.join(root, "event_v1.json"), "r") as f:
    event_v1 = json_loads(f.read().encode("utf-8"))

with open(os.path.join(root, "event_v2.json"), "r") as f:
    event_v2 = json_loads(f.read().encode("utf-8"))
