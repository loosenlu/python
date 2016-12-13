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
        pass


    def __parse_lua_basic_exp(self, cur_index):
        pass


    def __parse_lua_compound_exp(self, cur_index):
        pass


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
            compound expression meas this form exp:
                [exp1] = exp2
        and the other situations are invalid.
        """

        token_container = []
        is_dict = False
        length = len(self.lua_table_str)
        cur_index = self.__skip_unrelated_partition(cur_index)
        if self.lua_table_str[cur_index] != '{':
            raise LuaError("The lua table is invalid!")
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
                (cur_index, string_results)  = self.__parse_lua_string(cur_index)
            elif self.lua_table_str[cur_index] == '[':
                # for [exp1] = exp2
                (cur_index, compound_exp_result) = self.__parse_lua_compound_exp(cur_index)
            elif self.lua_table_str[cur_index] == '=':
                # for name = exp
                cur_index += 1
                key = token_container.pop()
                (cur_index, value) = self.__parse_lua_basic_exp(cur_index)
                item = DictItem(key, value)
                token_container.append(item)
            elif (self.lua_table_str[cur_index] == '_' or
                  self.lua_table_str[cur_index].isalpha()):
                (cur_index, basic_exp_result) = self.__parse_lua_basic_exp(cur_index)
            else:
                raise LuaError("The lua table is invalid!")



    def __parse_token(self, cur_index):

        length = len(self.lua_table_str)
        if self.lua_table_str[cur_index] == '[':
            cur_index += 1
            cur_index = self.__skip_unrelated_partition(cur_index)
            if self.lua_table_str[cur_index] == '[':
                # for string [[string]]
                token_beg = cur_index + 1
                cur_index = self.__find_matched_str(token_beg, "]]")
                token_end = cur_index
                cur_index += 2
                return (cur_index, self.__parse_lua_str_data(token_beg, token_end))
            elif self.lua_table_str[cur_index] == '=':
                # for string[===[string]===]
                equil_sign_num = 0
                while (cur_index < length and
                        self.lua_table_str[cur_index] == '='):
                    equil_sign_num += 1
                    cur_index += 1
                if (cur_index == length and
                        self.lua_table_str[cur_index] != '['):
                    raise LuaError("The lua table is invailed")
                token_beg = cur_index + 1
                cur_index = self.__find_matched_str(token_beg,
                                                    ']' + '=' * equil_sign_num + ']')
                token_end = cur_index
                cur_index += 2 + equil_sign_num
                return (cur_index, self.__parse_lua_str_data(token_beg, token_end))
            else:
                # for [key] = value
                token_beg = cur_index
                cur_index = self.__find_matched_str(token_beg, ']')
                token_end = cur_index
                cur_index += 1


        elif (self.lua_table_str[cur_index] == '"' or
              self.lua_table_str[cur_index] == "'"):
            # need to skip the comments??????
            token_beg = cur_index + 1
            cur_index = self.__find_matched_str(token_beg,
                                                self.lua_table_str[cur_index])
            token_end = cur_index
            cur_index += 1
            return (cur_index, self.__parse_lua_str_data(token_beg, token_end))
        else:
            delimeters = set(",;}= ")
            token_beg = cur_index
            while (cur_index < length and
                   self.lua_table_str[cur_index] not in delimeters):
                cur_index += 1

            token_end = cur_index
            cur_index = cur_index + 1 if cur_index != length else length - 1
            return (cur_index, self.__parse_lua_other_data(token_beg, token_end))



    
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