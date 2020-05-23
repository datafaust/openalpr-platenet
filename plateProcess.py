import json
from openalpr import Alpr
import sys
import os

#alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/openalpr/runtime_data/")

#alpr = Alpr("us", "~/etc/openalpr/openalpr.conf", "/runtime_data/")


def plateProcessor(plate):
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "openalpr/runtime_data/")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    
    #alpr.set_top_n(20)
    #alpr.set_default_region("md")

    results = alpr.recognize_file(plate)
    #print(json.dumps(results, indent=4))

    # Call when completely done to release memory
    alpr.unload()

    print(results['results'][0]['plate'])
    return results['results'][0]['plate']

#processPlate("srv/openalpr/ea7the.jpg")