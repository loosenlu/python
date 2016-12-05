


def extrat_dict_item(lua_table, start_index):
    '''
        return  dict_item(string format)
    '''
    cur_index = start_index
    left_braket_num = 0
    while cur_index < len(lua_table):

        if lua_table[cur_index] == '{':
            left_braket_num += 1
        elif lua_table[cur_index] == '}':
            left_braket_num -= 1
            # It means the '{' is marched
            if left_braket_num == 0:
                break

    return cur_index



def str_resolve(lua_table):

    is_dict = False
    component_container = []
    cur_index = pre_index = 0
    while cur_index < len(lua_table):

        if lua_table[cur_index] == '=':
            is_dict = True
            dict_item_key = lua_table[pre_index:cur_index]
            dict_item_value = lua_table[cur_index + 1:
                                        extrat_dict_item(lua_table, cur_index + 1)]
            component_container.append({dict_item_key:dict_item_value})
        



lua_table = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
l = str_resolve
            