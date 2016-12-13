import copy


class LuaError(Exception):
    """Raise for lua table is invalid"""
    pass


class DictItem(object):

    def __init__(self, first, second):
        self.key = first
        self.value = second


class PyLuaTblParser(object):
    """The PyLuaTblParser is used to convert between lua table
    (string format) and python dict.
    Parse the lua table(string format) and stored in a python dict;
    Or convert the python dict into a lua table.
    Attributes:
    """
    def __init__(self, lua_table=""):
        self.lua_table_str = lua_table
        if self.lua_table_str == "":
            self.lua_table_dict = {}
            self.consistancy = True


    def __skip_whitespaces(self, cur_index):
        while (cur_index < len(self.lua_table_str) and
               self.lua_table_str[cur_index].isspace()):
            cur_index += 1
        return cur_index


    def __skip_lua_comments(self, cur_index):
        """skip the lua comments
        In lua, there has 2 kind of comments
        1. line comments;
            -- line comments\n
        2. block comments
            a). --[[ comments block]]
            b). --[===[ comments block ]===]
        """


    def __skip_unrelated_partition(self, cur_index):
        cur_index = self.__skip_whitespaces(cur_index)
        # comments '--'
        if self.lua_table_str[cur_index:cur_index+2] == '--':
            cur_index = self.__skip_lua_comments(cur_index)
            cur_index = self.__skip_whitespaces(cur_index)
        return cur_index



    def __parse_lua_string(self, cur_index):
        """Parse the lua string

        About lua string, there also has 3 forms:
        1. "string"
        2. 'string'
        3. [[string]]
        """
        length = len(self.lua_table_str)
        if (self.lua_table_str[cur_index] == '"' or
            self.lua_table_str[cur_index] == "'"):
            # FOR "string" or 'string'
            end_lable = self.lua_table_str[cur_index]
            cur_index += 1
            str_beg_index = cur_index
            cur_index = self.lua_table_str.find(end_lable, cur_index)
            if cur_index == -1:
                raise LuaError("Lua table is invalid!")
            else:
                string_result = self.lua_table_str[str_beg_index:cur_index]
                cur_index += 1
                return (cur_index, string_result)
        else:
            # FOR [[string]]
            end_lable = "]]"
            cur_index += 2
            str_beg_index = cur_index
            cur_index = self.lua_table_str.find(end_lable, cur_index)
            if cur_index == -1:
                raise LuaError("Lua table is invalid!")
            else:
                string_result = self.lua_table_str[str_beg_index:cur_index]
                cur_index += 2
                return (cur_index, string_result)


    def __parse_lua_basic_exp(self, cur_index):
        """Parse the basic expression

        The basic expression has 5 situation:
        1. nil
        2. bool--> false, true
        3. number--> int, float
        4. string
        5. table
        """

        if (self.lua_table_str[cur_index] == '"' or
            self.lua_table_str[cur_index] == "'" or
            self.lua_table_str[cur_index:cur_index+2] == "[["):
            (cur_index, string_result) = self.__parse_lua_string(cur_index)
            return (cur_index, string_result)
        elif self.lua_table_str[cur_index] == '{':
            (cur_index, table_result) = self.__parse_lua_table(cur_index)
            return (cur_index, table_result)
        elif self.lua_table_str[cur_index] == '0123456789':
            pass
        elif self.lua_table_str[cur_index] == 't':
            return (cur_index + 4, True)
        elif self.lua_table_str[cur_index] == 'f':
            return (cur_index + 5, False)
        elif self.lua_table_str[cur_index] == 'n': # nil
            return (cur_index + 3, None)
        else:
            raise LuaError("Lua table is invalid!")


    def __parse_lua_compound_exp(self, cur_index):
        """Parse the compound expression

        [exp1] = exp2:
            In this program, we assume:
            a). exp1 belongs to either number(int or float) or string;
            b). exp2 belongs to nil, bool(true, flase), number, string,
                or table;
        """
        cur_index += 1
        cur_index = self.__skip_unrelated_partition(cur_index)
        (cur_index, exp1) = self.__parse_lua_basic_exp(cur_index)
        cur_index = self.__skip_unrelated_partition(cur_index)
        if self.lua_table_str[cur_index] != ']':
            raise LuaError("Lua table is invalid!")

        cur_index += 1
        cur_index = self.__skip_unrelated_partition(cur_index)
        if self.lua_table_str[cur_index] != '=':
            raise LuaError("Lua table is invalid!")
        cur_index = self.__skip_unrelated_partition(cur_index)

        (cur_index, exp2) = self.__parse_lua_basic_exp(cur_index)
        compound_exp = DictItem(exp1, exp2)
        return (cur_index, compound_exp)


    def __parse_lua_table(self, cur_index):
        """Parse the lua table(string format)
        About lua table constructors, there has 3 forms:
        1. [exp1] = exp2:
            In this program, we assume:
            a). exp1 belongs to either number(int or float) or string;
            b). exp2 belongs to nil, bool(true, flase), number, string,
                or table;
        2. name = exp:
            is equal to ["name"] = exp;
            name actually is a identifier--underline, number, letters
        3 exp1, exp2, ..., expn:
            each exp belongs to nil, bool(true, flase), number, string;
        About lua string, there also has 3 forms:
        1. "string"
        2. 'string'
        3. [[string]]
        Hence, There has several function to parse lua table
        1. string --> __parse_lua_string
        2. basic expression --> __parse_lua_basic_exp
        3. compound expression --> __parse_compound_exp
            compound expression meas this kind of expression:
                [exp1] = exp2
        and the other situations are invalid.
        """

        token_container = []
        is_dict = False
        length = len(self.lua_table_str)
        cur_index = self.__skip_unrelated_partition(cur_index)
        if self.lua_table_str[cur_index] != '{':
            raise LuaError("Lua table is invalid!")
        cur_index += 1

        while cur_index < length:

            cur_index = self.__skip_unrelated_partition(cur_index)

            if self.lua_table_str[cur_index] == '}':
                # Table end
                if is_dict:
                    token_container = PyLuaTblParser.__list2dict(
                        token_container)
                return (cur_index + 1, token_container)
            elif self.lua_table_str[cur_index] == '{':
                # Nested table
                (cur_index, nested_table_result) = self.__parse_lua_table(cur_index)
                token_container.append(nested_table_result)
            elif (self.lua_table_str[cur_index] == '"' or
                  self.lua_table_str[cur_index] == "'" or
                  self.lua_table_str[cur_index:cur_index+2] == "[["):
                # string
                (cur_index, string_results) = self.__parse_lua_string(cur_index)
                token_container.append(string_results)
            elif self.lua_table_str[cur_index] == '[':
                # for [exp1] = exp2
                (cur_index, compound_exp_result) = \
                        self.__parse_lua_compound_exp(cur_index)
                token_container.append(compound_exp_result)
            elif self.lua_table_str[cur_index] == '=':
                # for name = exp
                cur_index += 1
                key = token_container.pop()
                (cur_index, value) = self.__parse_lua_basic_exp(cur_index)
                item = DictItem(key, value)
                token_container.append(item)
            elif (self.lua_table_str[cur_index] == '_' or
                  self.lua_table_str[cur_index].isalpha()):
                (cur_index, basic_exp_result) = \
                        self.__parse_lua_basic_exp(cur_index)
                token_container.append(basic_exp_result)
            else:
                raise LuaError("Lua table is invalid!")

            cur_index = self.__skip_unrelated_partition(cur_index)
            if (self.lua_table_str[cur_index] == ',' or
                    self.lua_table_str[cur_index] == ';'):
                cur_index += 1
            elif self.lua_table_str[cur_index] == '}':
                continue
            else:
                raise LuaError("Lua table is invalid!")
        raise LuaError("Lua table is invalid!")




    @classmethod
    def __list2dict(cls, list_data):
        """convert list to dict
        """
        dict_data = {}
        index = 1
        for item in list_data:
            if isinstance(item, DictItem):
                if not dict_data.has_key(item.key):
                    dict_data[item.key] = item.value
            else:
                dict_data[index] = item
                index += 1
        return dict_data
