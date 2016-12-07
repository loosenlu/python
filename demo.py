

def parse_lua_table(lua_table):
    """parse lua table and stored in a python sequence type.

    parse the lua table. if the lua table contain [key] = Value
    return a dict, else return a list.

    Args:
        lua_table: a lua table that need to parse
    Returns:
        A dict or list that contains all items in lua table
    """

    is_dict = False
    component_container = []
    pre_index = cur_index = 0

    # need to implement, delete the '{}'


    while cur_index < len(lua_table):

        if lua_table[cur_index] == '=':
            is_dict = True
            value_start, value_end = extract_dict_value(lua_table, 
                                                        cur_index + 1)
            dict_key = lua_table[pre_index:cur_index].strip()
            dict_key = str2num(dict_key)
            dict_value = lua_table[value_start:value_end]
            dict_value = parse_lua_table(dict_value)
            component_container.append({dict_key:dict_value})

            pre_index = value_end + 1
            cur_index = pre_index
            continue
        elif lua_table[cur_index] == ',':
            if (cur_index == pre_index):
                cur_index += 1
                pre_index = cur_index
                continue
            list_item = lua_table[pre_index:cur_index].strip()
            component_container.append(str2num(list_item))
            pre_index = cur_index + 1
        
        cur_index += 1
            


def extract_dict_value(table_str, start_index):
    """ todo
    """
    # judge whether the dict value part in a pair of braces
    first_leftbrace_index = table_str.find(start_index, '{')
    first_comma_index = table_str.find(start_index, ',')
    if (first_comma_index < first_leftbrace_index or
            first_leftbrace_index == -1):
        return start_index, first_comma_index

    leftbrace_num = 1
    cur_index = first_leftbrace_index
    while cur_index < len(table_str):

        if table_str[cur_index] == '{':
            leftbrace_num += 1
        elif table_str[cur_index] == '}':
            leftbrace_num -= 1
            if leftbrace_num == 0:
                break
    return first_leftbrace_index, cur_index


def is_int(number_str):
    try:
        int(number_str)
        return True
    except: ValueError:
        return False


def is_float(number_str):
    try:
        float(number_str):
        return True
    except: ValueError:
        return False

    
def str2num(number_str):
    if is_int(number_str):
        return int(number_str)
    elif is_float(number_str):
        return float(number_str)
    else:
        return number_str