


def extrat_dict_item(lua_table, start_index):
    '''
        return  a dict_item range[start_index, end_index)
    '''
    cur_index = start_index
    first_comma_index = lua_table.find(',', start_index)
    first_braket_index = lua_table.find('{', start_index)
    if first_comma_index < first_braket_index | first_comma_index == -1:
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



def str_resolve(lua_table):

    is_dict = False
    component_container = []
    cur_index = pre_index = 0
    while cur_index < len(lua_table):

        if lua_table[cur_index] == '=':

            is_dict = True
            dict_item_key = lua_table[pre_index:cur_index]

            item_start, item_end = extrat_dict_item(lua_table, cur_index + 1)
            dict_item_value = lua_table[item_start: item_end]
            component_container.append({dict_item_key.strip():dict_item_value.strip()})
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
    return component_container



lua_table = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,9,string = "value",},\
                array = {3,6,4,},string = "value",},}'
l = str_resolve(lua_table)
print l