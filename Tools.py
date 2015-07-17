import json


def initConfigInfo():
    f = open("config.json", "r")
    config = json.load(f)
    f.close()
    return config
