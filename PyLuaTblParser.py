
import copy


class PyLuaTblParser(object):
    """The PyLuaTblParser is used to convert between
    lua table(string format) and python dict.

    Parse the lua table(string format) and stored in a
    python dict; Or convert the python dict into a lua table.

    Attributes:

    """
    def __init__(self, lua_table=''):
        self.lua_table = lua_table
        if self.lua_table == '':
            self.lua_table_dict = {}
            self.consistency = True
        else:
            # check whether lua_table is a valid
            # lua table string.
            if PyLuaTblParser.__is_lua_table(self.lua_table):
                self.lua_table_dict = \
                    PyLuaTblParser.__parse_lua_table(self.lua_table)
                self.consistency = True
            else:
                raise ValueError, "The init lua table is invalid!"


    def load(self, s):
        """load a lua table(string format)

        if lua table is invalid, will raise a ValueError.
        """
        if PyLuaTblParser.__is_lua_table(s):
            self.lua_table = s
            self.lua_table_dict = \
                PyLuaTblParser.__parse_lua_table(self.lua_table)
            self.consistency = True
        else:
            raise ValueError, "The load string is invalid!"


    def dump(self):
        """return the lua table(string format)

        self.consistency indicate whether the lua_table is
        latest.
        """
        if not self.consistency:
            self.__synchronize_lua_table()
        return self.lua_table


    def loadDict(self, d):
        """load a python dict and update.

        """
        self.lua_table_dict = copy.deepcopy(d)
        self.__update_lua_table_dict()
        self.consistency = False


    def dumpDict(self):
        """return a python dict

        """
        return copy.deepcopy(self.lua_table_dict)


    def loadLuaTable(self, f):
        """load a lua table(string format) from a file.
        
        """
        


    def __getitem__(self, index):
        try:
            return self.lua_table_dict[index]
        except IndexError, KeyError:
            raise KeyError, "Don't have keyword!'"


    def __setitem__(self, index, value):

        if isinstance(self.lua_table_dict, list):
            item_container = {}
            cur_index = 0
            while cur_index < len(self.lua_table_dict):
                item_container[cur_index + 1] = \
                    self.lua_table_dict[cur_index]
                cur_index += 1
            self.lua_table_dict = item_container
        self.lua_table_dict[index] = value
        self.consistency = False


    def update(self, update_dict):

        if isinstance(self.lua_table_dict, list):
            item_container = {}
            cur_index = 0
            while cur_index < len(self.lua_table_dict):
                item_container[cur_index + 1] = \
                    self.lua_table_dict[cur_index]
                cur_index += 1
            self.lua_table_dict = item_container
        self.lua_table_dict.update(update_dict)
        self.__update_lua_table_dict()
        self.consistency = False


    def __update_lua_table_dict(self):

        for i in self.lua_table_dict.iterkeys():
            if not (isinstance(i, int) or
                    isinstance(i, float) or
                    isinstance(i, str)):
                del self.lua_table_dict[i]


    def __synchronize_lua_table(self):

        self.lua_table = \
            PyLuaTblParser.__parse_python_data(self.lua_table_dict)
        self.consistency = True


    @staticmethod
    def __is_lua_table(lua_table):
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
            cur_index += 1

        cur_index = last_right_brace_index + 1
        while cur_index < len(lua_table):
            if not lua_table[cur_index].isspace():
                return False
            cur_index += 1

        cur_index = left_brace_number = 0
        while cur_index < len(lua_table):
            if lua_table[cur_index] == '{':
                left_brace_number += 1
            elif lua_table[cur_index] == '}':
                left_brace_number -= 1
            cur_index += 1

        return (True if left_brace_number == 0
                else False)


    @staticmethod
    def __parse_lua_table(lua_table):
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
                value_start, value_end = \
                    PyLuaTblParser.__acquire_dict_value_range(lua_table,
                                                              cur_index + 1)
                dict_key = lua_table[pre_index:cur_index].strip()
                dict_key = PyLuaTblParser.__extract_dict_key(dict_key)
                dict_value = lua_table[value_start:value_end]
                dict_value = PyLuaTblParser.__parse_lua_table(dict_value)

                pre_index = value_end
                cur_index = pre_index

                if not dict_value is None:
                    component_container.append({dict_key:dict_value})
                continue

            elif lua_table[cur_index] == ',':
                if cur_index == pre_index:
                    cur_index += 1
                    pre_index = cur_index
                    continue
                list_item = lua_table[pre_index:cur_index].strip()
                component_container.append(
                    PyLuaTblParser.__item_convert(list_item))
                pre_index = cur_index + 1

            cur_index += 1

        if is_dict:
            return PyLuaTblParser.__list2dict(component_container)
        if len(component_container) == 1:
            return component_container[0]
        return component_container


    @staticmethod
    def __acquire_dict_value_range(table_str, start_index):
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


    @staticmethod
    def __extract_dict_key(key_str):
        """extract dict items' key partition.

        lua table key has several format:
        1. [key] = value;
        2. ["key"] = Value;
        3. key = value
        """
        key_str = key_str.strip()
        if key_str[0] == '[' and key_str[-1] == ']':
            key_str = key_str.strip("[]")
            if key_str[0] == '"' and key_str[-1] == '"':
                key_str = key_str.strip('""')
                return key_str
            elif PyLuaTblParser.__is_int(key_str):
                return int(key_str)
            elif PyLuaTblParser.__is_float(key_str):
                return float(key_str)
        else:
            return key_str


    @staticmethod
    def __is_int(number_str):
        try:
            int(number_str)
            return True
        except ValueError:
            return False


    @staticmethod
    def __is_float(number_str):
        try:
            float(number_str)
            return True
        except ValueError:
            return False


    @staticmethod
    def __item_convert(item_str):
        """convert the value to appropriate type.

        Here, There are 4 data types:
        number(int, float), bool ,string, nil

        Args:
            item_str: a base item(string format)
        Returns:
            return a appropriate python type
        """
        # number type
        if PyLuaTblParser.__is_int(item_str):   # int
            return int(item_str)
        elif PyLuaTblParser.__is_float(item_str):   # float
            return float(item_str)
        # bool type
        elif item_str == "true":
            return True
        elif item_str == "false":
            return False
        # nil
        elif item_str == 'nil':
            return None
        # string
        else:
            # For string value, delete the '' and ""
            return item_str.strip("''\"\"")


    @staticmethod
    def __list2dict(needto_convert_list):

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


    @staticmethod
    def __parse_python_data(python_data):

        if python_data is None:
            return "nil"
        elif python_data is True:
            return "true"
        elif python_data is False:
            return "false"
        elif isinstance(python_data, str):
            return ''.join(['"', python_data, '"'])
        elif (isinstance(python_data, int) or
              isinstance(python_data, float)):
            return str(python_data)
        elif isinstance(python_data, dict):
            return PyLuaTblParser.__parse_python_dict(python_data)
        elif isinstance(python_data, list):
            return PyLuaTblParser.__parse_python_list(python_data)


    @staticmethod
    def __parse_python_dict(python_dict_data):

        items_container = []
        for key, value in python_dict_data.items():
            if isinstance(key, int):
                key_str = ''.join(['[', str(key), ']'])
                value_str = PyLuaTblParser.__parse_python_data(value)
                items_container.append(''.join([key_str, " = ", value_str]))
            elif isinstance(key, str):
                key_str = key
                value_str = PyLuaTblParser.__parse_python_data(value)
                items_container.append(''.join([key_str, " = ", value_str]))
            else:
                continue
        return ''.join(['{', ','.join(items_container), '}'])


    @staticmethod
    def __parse_python_list(python_list_data):

        items_container = []
        for value in python_list_data:
            if value is None:
                items_container.append("nil")
            elif value is True:
                items_container.append("true")
            elif value is False:
                items_container.append("false")
            else:
                items_container.append(str(value))
        return ''.join(['{', ','.join(items_container), '}'])

