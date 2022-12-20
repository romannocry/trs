from unicornException import UnicornException
from collections.abc import MutableMapping

def dict_compare(objectModel, payloadModel):

    #plainEnum
        #{'type': 'string', 'enum': ['foo', 'bar', 'foobar']}
    #rating
        #{'type': 'integer'}
    #oneOfMultiEnum
        #{'type': 'array', 'uniqueItems': True, 'items': {'oneOf': [{'const': 'foo', 'title': 'My Foo'}, {'const': 'bar', 'title': 'My Bar'}, {'const': 'jo', 'title': 'Mye Bar'}, {'const': 'foobar', 'title': 'My FooBar'}]}}
    #date
        #{'type': 'string', 'format': 'date', 'description': 'schema-based date picker'}
    payload = {}
    #iterating trhough the model's keys and acceptable values
    required_keys = objectModel['required']
    print(objectModel['properties'])
    print(type(objectModel['properties']))
    for k,v in objectModel['properties'].items():
        print(k, '->', v)
        #if key exists in the payload - check that the value is authorized
        print(k in payloadModel.keys())
        if k in payloadModel.keys():
            #if the model attribute is a list, use "in"
            if 'enum' in v.keys() and (isinstance(payloadModel[k],int) or isinstance(payloadModel[k],str)):
                print("is enum")
                if payloadModel[k] in v['enum'] or not v['enum']:
                    print("payload "+ str(payloadModel[k]) + " authorized in model")
                    payload[k] = payloadModel[k]
                else: 
                    print("payload "+ str(payloadModel[k]) + " NOT authorized in model, values expected in: "+str(v['enum'])+", value received:"+str(payloadModel[k])+" of type:"+str(type(payloadModel[k])))
                    raise UnicornException(name=payloadModel[k],label="invalid payload, values expected in: "+str(v['enum'])+", value received:"+str(payloadModel[k])+" of type:"+str(type(payloadModel[k])))
           #if not a list, then it is an open type *integer* *datetime*
            elif 'items' in v.keys():
                print("is multi item")
                data = []
                for item in payloadModel[k]:
                    lookup = any(x['const'] == item for x in v['items']['oneOf'])
                    if lookup:
                        print("payload "+ str(item)+" authorized in model")
                        data.append(item)
                    else:
                        print("payload "+ str(item) + " NOT authorized in model, values expected in: "+str(v['items']['oneOf'])+", value received:"+str(item)+" of type:"+str(type(item)))
                        raise UnicornException(name=item,label="invalid payload, values expected in: "+str(v['items']['oneOf'])+", value received:"+str(item)+" of type:"+str(type(item)))
                payload[k] = data
            else:
                print("is not enum")
                if isinstance(payloadModel[k],eval(v['type'][0:3])):
                    print("payload "+ str(payloadModel[k]) + " authorized in model")
                    payload[k] = payloadModel[k]    
                else: 
                    print("payload "+ str(payloadModel[k]) + " NOT authorized in model, type expected: "+str(v['type'])+", type received:"+str(type(payloadModel[k])))
                    raise UnicornException(name=payloadModel[k],label="invalid payload, type expected:"+str(v['type'])+", type received:"+str(type(payloadModel[k])))
            ## NEED TO HANDLE MULTI ENUM ##
        else: #k in required_keys:
            if (k in required_keys):
            #should be able to push a subset of the data
                print("no data was pushed for required key '"+k+"'. Please review your payload")
                raise UnicornException(name=k,label="missing value for required field: '"+str(k)+"' of type "+str(v['type']))
            else:
                print("no data was pushed for key '"+k+"' but it was not mandatory")


    return payload

    #for k,v in objectModel['properties']:
    #    print("test")
        #all the object attributes and their type
     #   print(k)
      #  print("***")

        #for each key in the data model, find the one in the payload:
        #if missing but not required >> ok but send report
        #if missing and required >> impossible to persist
        # if present and not required (data not needed) >> do not persist value but process the rest
        #if present and required, all good

        #datatypes to handle: date, enums, string, integer, multiple choice input

        #if key exists in the payload - check that the value is authorized
    #    if k in payloadModel.keys():
            #if the model attribute is a list, use "in"
    #        if isinstance(v['values'],list):
    #            if payloadModel[k] in v['values'] or not v['values']:
    #                print("payload "+ str(payloadModel[k]) + " authorized in model")
    #                payload[k] = payloadModel[k]
    #            else: 
    #                print("payload "+ str(payloadModel[k]) + " NOT authorized in model, values expected in: "+str(v['values'])+", value received:"+payloadModel[k]+" of type:"+str(type(payloadModel[k])))
    #                raise UnicornException(name=payloadModel[k],label="invalid payload, values expected in: "+str(v['values'])+", value received:"+payloadModel[k]+" of type:"+str(type(payloadModel[k])))
            #if not a list, then it is an open type *integer* *datetime*
    #        else:
    #            if isinstance(payloadModel[k],eval(v['values'])):
    #                print("payload "+ str(payloadModel[k]) + " authorized in model")
    #                payload[k] = payloadModel[k]
    #            else: 
    #                print("payload "+ str(payloadModel[k]) + " NOT authorized in model, type expected: "+str(v['values'])+", type received:"+str(type(payloadModel[k])))
    #                raise UnicornException(name=payloadModel[k],label="invalid payload, type expected:"+str(v['values'])+", type received:"+str(type(payloadModel[k])))

    #    else:
    #        #should be able to push a subset of the data
    #        print("no data was pushed for key "+k+". Please review your payload")
    #        raise UnicornException(name=payloadModel,label="payload not fully matching object model, expected: "+str(objectModel))

    #return payload

def dict_compareBU(objectModel, payloadModel):

    #d1_keys = set(d1.keys())
    #print(d1_keys)
    #d2_keys = set(d2.keys())
    #print(d2_keys)
    #intersect_keys = d1_keys.intersection(d2_keys)
    #print(intersect_keys)
    #added = d1_keys - d2_keys
    #print(added)
    #removed = d2_keys - d1_keys
    #print(removed)
    #modified = {o : (d1[o], d2[o]) for o in intersect_keys if d2[o] in d1[o]}
    #print("modified")
    #print(modified)
    #same = set(o for o in intersect_keys if d1[o] == d2[o])
    #print(same)

    return added, removed, modified, same


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '_'):
    return dict(_flatten_dict_gen(d, parent_key, sep))

