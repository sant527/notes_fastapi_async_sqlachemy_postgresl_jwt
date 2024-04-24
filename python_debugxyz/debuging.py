########################################################################

# pretty print any obj
import json

def pprint_any_obj(obj):
    final_processed_obj = None
    if isinstance(obj,(dict,list,set,tuple)):
        final_processed_obj = flatten_anything(obj)
        print(json.dumps(final_processed_obj,indent=2,default=str))
        return

    # final_processed_obj = {k: getattr(obj,key) for k in dir(obj)}
    # we are not using the above is because if there are except it stops

    c_dict = {
        '00_METHODS********************************************************************************':{},
        "01_UNDESCORE******************************************************************************":{},
        "02_OTHERS*********************************************************************************":{},
        "03_EXCEPTIONS*****************************************************************************":{},
    }
    # level of checking for any errors in the obj



    for key in dir(obj):
        try:
            attr_obj = getattr(obj,key)
            if callable(attr_obj):
                c_dict["00_METHODS********************************************************************************"][key] = attr_obj
            else:
                if key.startswith("_"):
                    c_dict['01_UNDESCORE******************************************************************************'][key] = attr_obj
                else:
                    c_dict['02_OTHERS*********************************************************************************'][key] = attr_obj
        except Exception as x:
            c_dict['03_EXCEPTIONS*****************************************************************************'][key] = x

    final_processed_obj = flatten_anything(c_dict)
    print(json.dumps(final_processed_obj,indent=2,default=str))




def flatten_anything(obj):
    rval = {}
    if not isinstance(obj,(dict)):
        if isinstance(obj,(list,tuple,set)):
            return([flatten_anything(x) for x in obj])
        else:
            return obj

    keys = list(obj.keys())
    for k in keys:
        v = obj[k]
        if isinstance(k,bytes):
            k = k.decode()
        if isinstance(v,dict):
            v = flatten_anything(v)
        if isinstance(v,(list,tuple,set)):
            v = [flatten_anything(x) for x in v]
        rval[k] = v
    return rval



# install snoop for this
# https://github.com/alexmojaki/snoop
import snoop
from cheap_repr import find_repr_function
import six


def path(event):
    return event.code.co_filename[-20:]


find_repr_function(object).maxparts = 100000000
find_repr_function(dict).maxparts = 100000000
find_repr_function(list).maxparts = 100000000
find_repr_function(six.text_type).maxparts = 500000000
find_repr_function(six.binary_type).maxparts = 100000000


###############################################################################