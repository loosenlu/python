


def extrat_dict_item(lua_table, start_index):
    '''
        return  a dict_item range[start_index, end_index)
    '''
    cur_index = start_index
    first_comma_index = lua_table.find(',', start_index)
    first_braket_index = lua_table.find('{', start_index)
    if first_comma_index < first_braket_index or first_braket_index == -1:
        return start_index, first_comma_index


    left_braket_num = 0
    while cur_index < len(lua_table):

        if lua_table[cur_index] == '{':
            left_braket_num += 1
        elif lua_table[cur_index] == '}':
            left_braket_num -= 1
            # It means the '{' is marched
            if left_braket_num == 0:
                break
        cur_index += 1

    return first_braket_index + 1, cur_index



def list2dict(convert_list):
    '''
        return the converted dict
    '''
    converted_result = {}
    index = 1
    for i in convert_list:
        if isinstance(i, dict):
            key, value = i.items()[0]
            converted_result[key] = value
        else:
            converted_result[index] = i
            index += 1
    return converted_result



def preprocess_lua_table(lua_table):
    '''
        pre-process the lua, including
        check is a legal lua table
        and delete the start and end blank and '{}'
    '''
    lua_table = lua_table.strip()
    left_braket_num = 0
    for i in lua_table:
        if i == '{':
            left_braket_num += 1
        elif i == '}':
            left_braket_num -= 1
    # illegal lua table
    if left_braket_num != 0:
        raise Exception("The lua table is illegal!\n")
    return lua_table.strip(" {}")




def str_resolve(lua_table):


    lua_table = preprocess_lua_table(lua_table)
    has_dict = False
    component_container = []
    cur_index = pre_index = 0
    while cur_index < len(lua_table):

        if lua_table[cur_index] == '=':

            has_dict = True
            dict_item_key = lua_table[pre_index:cur_index].strip()

            item_start, item_end = extrat_dict_item(lua_table, cur_index + 1)
            dict_item_value = lua_table[item_start: item_end].strip()
            dict_item_value = str_resolve(dict_item_value)
            component_container.append({dict_item_key:dict_item_value})
            cur_index = item_end + 1
            pre_index = cur_index
            continue
        elif lua_table[cur_index] == ',':

            if pre_index == cur_index:
                cur_index += 1
                pre_index = cur_index
                continue
            list_item = lua_table[pre_index:cur_index]
            component_container.append(list_item.strip())
            pre_index = cur_index + 1
            cur_index += 1
            continue
        cur_index += 1

    if has_dict:
        component_container = list2dict(component_container)
    return component_container



test1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,9,string = "value",},\
                array = {3,6,4,},string = "value",},}'
test2 ='{mixed = {43,54.33,false,9,string = "value",},}'
l = str_resolve(test1)
print l