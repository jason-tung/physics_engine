from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, obj):
        d = {}
        # mxvw
        d["m"] = obj.m
        d["points"] = [tuple(k) for k in obj.points]
        # print("=====")
        return d
