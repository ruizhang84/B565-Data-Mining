# split the full path of a json file into fields
def parse_full_path(path : str):
    # a path is like /some_path/2017/11/01/00/00.json
    l = path.split('/')
    return l[-5:]
