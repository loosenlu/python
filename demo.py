

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
    lua_table = lua_table.strip(' {}')

    while cur_index < len(lua_table):

        if lua_table[cur_index] == '=':
            is_dict = True
            value_start, value_end = extract_dict_value(lua_table,
                                                        cur_index + 1)
            dict_key = lua_table[pre_index:cur_index].strip()
            dict_key = subscript_convert(dict_key)
            dict_value = lua_table[value_start:value_end]
            dict_value = parse_lua_table(dict_value)

            pre_index = value_end + 1
            cur_index = pre_index

            if dict_value != None:
                component_container.append({dict_key:dict_value})
            continue

        elif lua_table[cur_index] == ',':
            if cur_index == pre_index:
                cur_index += 1
                pre_index = cur_index
                continue
            list_item = lua_table[pre_index:cur_index].strip()
            component_container.append(value_convert(list_item))
            pre_index = cur_index + 1

        cur_index += 1

    if is_dict:
        return list2dict(component_container)
    if len(component_container) == 1:
        return component_container[0]
    return component_container

def extract_dict_value(table_str, start_index):
    """ todo
    """
    # judge whether the dict value part in a pair of braces
    first_leftbrace_index = table_str.find('{', start_index)
    first_comma_index = table_str.find(',', start_index)
    if (first_comma_index < first_leftbrace_index or
            first_leftbrace_index == -1):
        return start_index, first_comma_index + 1

    leftbrace_num = 0
    cur_index = first_leftbrace_index
    while cur_index < len(table_str):

        if table_str[cur_index] == '{':
            leftbrace_num += 1
        elif table_str[cur_index] == '}':
            leftbrace_num -= 1
            if leftbrace_num == 0:
                break
        cur_index += 1
    # return a index range
    # that contain ['{',...,'}'+1)
    return first_leftbrace_index, cur_index + 1


def is_int(number_str):
    try:
        int(number_str)
        return True
    except ValueError:
        return False


def is_float(number_str):
    try:
        float(number_str)
        return True
    except ValueError:
        return False


def subscript_convert(subscript_str):
    if is_int(subscript_str):
        return int(subscript_str)
    elif is_float(subscript_str):
        return float(subscript_str)
    else:
        return subscript_str


def value_convert(value_str):
    """convert the value to appropriate type.

    Here, There are four different situation:
    bool, number, string, nil

    Args:
        value_str: a value_str
    Returns:
        return a appropriate format
    """
    if is_int(value_str):   # int
        return int(value_str)
    elif is_float(value_str):   # float
        return float(value_str)
    elif value_str == "true":   # bool value
        return True
    elif value_str == "false":
        return False
    elif value_str == 'nil':
        return None
    else:
        # For string value, delete the '' and ""
        return value_str.strip("''\"\"")



def list2dict(needto_convert_list):

    index = 1
    converted_result = {}
    for i in needto_convert_list:
        if isinstance(i, dict):
            key, value = i.items()[0]
            converted_result[key] = value
        else:
            converted_result[index] = i
            index += 1
    return converted_result


def is_lua_table(lua_table):
    """check whether the lua table is legal

    Here, this function mainly check two kind of errors.
    1. Braces are not martch;
    2. "xxxx{}xxxx". x represents letters.

    Args:
        lua_table: a lua_table need to check
    Returns:
        a bool value
    """
    first_left_brace_index = lua_table.find('{')
    last_right_brace_index = lua_table.rfind('}')
    if (first_left_brace_index == -1 or
            last_right_brace_index == -1):
        return False

    cur_index = 0
    while cur_index < first_left_brace_index:
        if not lua_table[cur_index].isspace():
            return False

    cur_index = last_right_brace_index
    while cur_index < len(lua_table):
        if not lua_table[cur_index].isspace():
            return False

    cur_index = left_brace_number = 0
    while cur_index < len(lua_table):
        if lua_table[cur_index] == '{':
            left_brace_number += 1
        elif lua_table[cur_index] == '}':
            left_brace_number -= 1

    return (True if left_brace_number == 0
            else False)


test_str1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,nil,string = "value",},\
            array = {3,6,4,},string = nil,},}'
result = parse_lua_table(test_str1)
print result