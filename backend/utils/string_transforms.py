import re
import json

def string_to_dict(string_input):

    try:
        res = re.findall("\{(.*?)\}", string_input)
        for i in range(len(res)):
            res[i] = ''.join(("{",res[i],"}"))
            res[i] = re.sub("\'", "\"", res[i])
            res[i] = json.loads(res[i])
            return res
    except:
        return None


def string_to_list(string_input):

    res = string_input.split("|")
    return(res)