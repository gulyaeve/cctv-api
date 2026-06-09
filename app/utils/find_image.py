import os
import re


def find_screenshot(incident_id: int, camera_id: int, search_dir: str = "screenshots_bank"):
    pattern = re.compile(f"^{incident_id}_.*?_{camera_id}_.*?\\.jpg$")
    for filename in os.listdir(search_dir):
        if pattern.match(filename):
            return filename