import copy


class LuaError(Exception):
    """Raise for lua table is invalid"""
    pass


class PythonTypeError(Exception):
    """Raise if there has python type Error"""
    pass


class Pairs(object):

    def __init__(self, first, second):
        self.first = first
        self.second = second


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
        else:
            end_index, self.lua_table_dict = self.__parse_lua_table(0)
        self.consistancy = True


    def load(self, s):
        """Load the s as lua table(string format)

        """
        self.lua_table_str = s
        end_index, self.lua_table_dict = self.__parse_lua_table(0)


    def dump(self):
        """Return the lua table(string format)

        """
        if not self.consistancy:
            self.lua_table_str = \
                PyLuaTblParser.__parse_python_value(self.lua_table_dict)
        return self.lua_table_str


    def loadDict(self, d):
        """pass

        """
        self.lua_table_dict = copy.deepcopy(d)
        self.consistancy = False


    def dumpDict(self):
        """pass

        """
        return copy.deepcopy(self.lua_table_dict)


    def loadLuaTable(self, f):
        """pass

        """
        with open(f, 'r') as f_oject:
            lua_table = f_oject.read()
            self.__init__(lua_table)


    def dumpLuaTable(self, f):
        """pass

        """
        if not self.consistancy:
            self.lua_table_str = \
                PyLuaTblParser.__parse_python_value(self.lua_table_dict)
        with open(f, 'w') as f_oject:
            f_oject.write(self.lua_table_str)
        


    def __getitem__(self, index):
        pass


    def __setitem__(self, index, value):
        pass


    def update(self, update_dict):
        pass


    def __skip_whitespaces(self, cur_index):
        while (cur_index < len(self.lua_table_str) and
               self.lua_table_str[cur_index].isspace()):
            cur_index += 1
        return cur_index


    def __skip_lua_comments(self, cur_index):
        """skip the lua comments
        In lua, there has 2 kinds of comments
        1. line comments;
            -- line comments\n
        2. block comments
            --[[ comments block]]
        """
        if self.lua_table_str[cur_index:cur_index+4] == '--[[':
            # block comments
            cur_index += 4
            cur_index = self.lua_table_str.find("]]", cur_index)
            if cur_index == -1:
                raise LuaError("Lua table is invalid!")
            return cur_index + 2
        else:
            # line comments
            cur_index += 2
            cur_index = self.lua_table_str.find("\n", cur_index)
            if cur_index == -1:
                raise LuaError("Lua table is invalid!")
            return cur_index + 1


    def __skip_unrelated_partition(self, cur_index):
        cur_index = self.__skip_whitespaces(cur_index)
        # comments '--'
        if self.lua_table_str[cur_index:cur_index+2] == '--':
            cur_index = self.__skip_lua_comments(cur_index)
            cur_index = self.__skip_whitespaces(cur_index)
        return cur_index



    def __parse_lua_string_unit(self, cur_index):
        """Parse the lua string unit(without concat)

        About lua string, there also has 3 forms:
        1. "string"
        2. 'string'
        3. [[string]]
        """

        length = len(self.lua_table_str)
        if (self.lua_table_str[cur_index] == '"' or
            self.lua_table_str[cur_index] == "'"):
            # FOR "string" or 'string'
            escape_dict = {
                "\\a" : '\a',    # '\a' (bell),
                "\\b" : '\b',    # '\b' (backspace),
                "\\f" : '\f',    # '\f' (form feed),
                "\\n" : '\n',    # '\n' (newline),
                "\\r" : '\r',    # '\r' (carriage return),
                "\\t" : '\t',    # '\t' (horizontal tab),
                "\\v" : '\v',    # '\v' (vertical tab),
                "\\\\" : '\\',   #'\\' (backslash),
                '\\"' : '\"',    # '\"' (double quote),
                "\\'" : '\'',    # '\'' (single quote).
            }
            letter_container = []
            end_lable = self.lua_table_str[cur_index]
            cur_index += 1
            while (cur_index < length and
                   self.lua_table_str[cur_index] != end_lable):
                if self.lua_table_str[cur_index] == '\\':
                    escape_letter = self.lua_table_str[cur_index:cur_index+2]
                    if escape_letter in escape_dict:
                        letter_container.append(escape_dict[escape_letter])
                        cur_index += 2
                    else:
                        raise LuaError("Lua table is invalid!")
                else:
                    letter_container.append(self.lua_table_str[cur_index])
                    cur_index += 1
            if self.lua_table_str[cur_index] != end_lable:
                raise LuaError("Lua table is invalid!")
            else:
                string_ressult = ''.join(letter_container)
                cur_index += 1
                return (cur_index, string_ressult)
        else:
            # FOR [[string]]
            end_lable = "]]"
            cur_index += 2
            str_beg_index = cur_index
            cur_index = self.lua_table_str.find(end_lable, cur_index)
            if cur_index == -1:
                raise LuaError("Lua table is invalid!")
            else:
                string_result = \
                    self.lua_table_str[str_beg_index:cur_index]
                cur_index += 2
                return (cur_index, string_result)


    def __parse_lua_string(self, cur_index):
        """Parse the lua string(with concat)

        And process string concat:
        "string1 " .. [[string2]] == "string1 string2"
        """
        length = len(self.lua_table_str)
        string_container = []
        while cur_index < length:
            (cur_index, string_item) = self.__parse_lua_string_unit(cur_index)
            string_container.append(string_item)
            cur_index = self.__skip_unrelated_partition(cur_index)
            if self.lua_table_str[cur_index:cur_index+2] != "..":
                break
            else:
                # FOR concat
                cur_index += 2
                cur_index = self.__skip_unrelated_partition(cur_index)
                if (self.lua_table_str[cur_index] == '"' or
                    self.lua_table_str[cur_index] == "'" or
                    self.lua_table_str[cur_index:cur_index+2] == "[["):
                    continue
                else:
                    # FOR "string" .. is invalid
                    raise LuaError("Lua table is invalid!")
        string_result = ''.join(string_container)
        return (cur_index, string_result)


    def __parse_lua_number(self, cur_index):
        """Parse lua number

        There are 2 kinds of number
        1. int--> +16, 0, -16,...;
        2. float--> 0.4, 4.57e-3, 0.3e12, 5e+20
        """
        sign = False
        length = len(self.lua_table_str)
        NUMBER_LETTER_SET = set("0123456789abcdefABCDEF.")
        if self.lua_table_str[cur_index] == '-':
            sign = True
            cur_index += 1

        if (self.lua_table_str[cur_index:cur_index+2] == "0x" or
            self.lua_table_str[cur_index:cur_index+2] == "0X"):
            cur_index += 2
            num_beg = cur_index
            dot_index = -1
            while (cur_index < length and
                   self.lua_table_str[cur_index] in NUMBER_LETTER_SET):
                if self.lua_table_str[cur_index] == '.':
                    dot_index = cur_index
                cur_index += 1
            # has dot
            if dot_index != -1:
                int_part_str = self.lua_table_str[num_beg:dot_index]
                int_part = int(int_part_str, 16)
                fraction_start = dot_index + 1
                fraction_end = cur_index - 1
                fraction_part = 0
                while fraction_start <= fraction_end:
                    fraction_part = (fraction_part
                                     + int(self.lua_table_str[fraction_end], 16)) / 16.0
                    fraction_end -= 1
                number_result = -1*(int_part + fraction_part) if sign else \
                    (int_part + fraction_part)
                return (cur_index, number_result)
        else:
            num_beg = cur_index
            while (cur_index < length and
                   self.lua_table_str[cur_index] in NUMBER_LETTER_SET):
                cur_index += 1
            num_str = self.lua_table_str[num_beg:cur_index]
            try:
                number_result = int(num_str)
                number_result = -1 * number_result if sign else number_result
                return (cur_index, number_result)
            except ValueError:
                try:
                    number_result = float(num_str)
                    number_result = -1 * number_result if sign else number_result
                    return (cur_index, number_result)
                except ValueError:
                    raise LuaError("Lua table is invalid!")



    def __parse_lua_basic_exp(self, cur_index):
        """Parse the basic expression

        The basic expression has 5 situation:
        1. nil
        2. bool--> false, true
        3. number--> int, float
        4. string
        5. table
        """
        NUMBER_START_LETTERS_SET = set("+-0123456789")

        if (self.lua_table_str[cur_index] == '"' or
            self.lua_table_str[cur_index] == "'" or
            self.lua_table_str[cur_index:cur_index+2] == "[["):
            # FOR string
            (cur_index, string_result) = self.__parse_lua_string(cur_index)
            return (cur_index, string_result)
        elif self.lua_table_str[cur_index] == '{':
            # FOR table
            (cur_index, table_result) = self.__parse_lua_table(cur_index)
            return (cur_index, table_result)
        elif self.lua_table_str[cur_index] in NUMBER_START_LETTERS_SET:
            #FOR number
            (cur_index, number_result) = self.__parse_lua_number(cur_index)
            return (cur_index, number_result)
        elif self.lua_table_str[cur_index: cur_index + 4] == "true":
            # FOR true
            return (cur_index + 4, True)
        elif self.lua_table_str[cur_index: cur_index + 5] == "false":
            # FOR false
            return (cur_index + 5, False)
        elif self.lua_table_str[cur_index: cur_index + 3] == "nil":
            # FOR nil
            return (cur_index + 3, None)
        else:
            # Invalid letter
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
        cur_index += 1
        cur_index = self.__skip_unrelated_partition(cur_index)

        (cur_index, exp2) = self.__parse_lua_basic_exp(cur_index)
        compound_exp = Pairs(exp1, exp2)
        return (cur_index, compound_exp)


    def __parse_lua_name(self, cur_index):
        """Parse lua name(identifier)

        Names (also called identifiers) in Lua can be any string of letters, digits,
        and underscores, not beginning with a digit and not being a reserved word.
        """
        length = len(self.lua_table_str)
        name_beg = cur_index
        while (cur_index < length and
               (self.lua_table_str[cur_index] == '_'
                or self.lua_table_str[cur_index].isalpha())):
            cur_index += 1
        return (cur_index, self.lua_table_str[name_beg:cur_index])


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
            name actually is a identifier--underscores, number, letters
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
        NUMBER_START_LETTERS_SET = set("-0123456789")
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
                # FOR Table end
                if is_dict:
                    token_container = PyLuaTblParser.__list2dict(
                        token_container)
                return (cur_index + 1, token_container)
            elif self.lua_table_str[cur_index] == '{':
                # FOR Nested table
                (cur_index, nested_table_result) = self.__parse_lua_table(cur_index)
                token_container.append(nested_table_result)
            elif (self.lua_table_str[cur_index] == '"' or
                  self.lua_table_str[cur_index] == "'" or
                  self.lua_table_str[cur_index:cur_index+2] == "[["):
                # FOR string
                (cur_index, string_results) = self.__parse_lua_string(cur_index)
                token_container.append(string_results)
            elif self.lua_table_str[cur_index] == '[':
                # FOR [exp1] = exp2
                is_dict = True
                (cur_index, compound_exp_result) = \
                        self.__parse_lua_compound_exp(cur_index)
                token_container.append(compound_exp_result)
            elif self.lua_table_str[cur_index] in NUMBER_START_LETTERS_SET:
                # FOR number
                (cur_index, number_result) = self.__parse_lua_number(cur_index)
                token_container.append(number_result)
            elif self.lua_table_str[cur_index:cur_index+5] == 'false':
                # FOR false
                cur_index += 5
                token_container.append(False)
            elif self.lua_table_str[cur_index:cur_index+4] == 'true':
                # FOR true
                cur_index += 4
                token_container.append(True)
            elif self.lua_table_str[cur_index:cur_index+3] == 'nil':
                # FOR nil
                cur_index += 3
                token_container.append(None)
            elif (self.lua_table_str[cur_index] == '_' or
                  self.lua_table_str[cur_index].isalpha()):
                # FOR name = exp
                is_dict = True
                (cur_index, name) = self.__parse_lua_name(cur_index)
                cur_index = self.__skip_unrelated_partition(cur_index)
                if self.lua_table_str[cur_index] != '=':
                    raise LuaError("Lua table is invalid!")
                cur_index += 1
                cur_index = self.__skip_unrelated_partition(cur_index)
                (cur_index, exp) = self.__parse_lua_basic_exp(cur_index)
                item = Pairs(name, exp)
                token_container.append(item)
            else:
                raise LuaError("Lua table is invalid!")

            cur_index = self.__skip_unrelated_partition(cur_index)
            if (self.lua_table_str[cur_index] == ',' or
                    self.lua_table_str[cur_index] == ';'):
                cur_index += 1
            elif self.lua_table_str[cur_index] == '}':
                # FOR table last item {,...,item}
                continue
            else:
                raise LuaError("Lua table is invalid!")
        raise LuaError("Lua table is invalid!")


    @classmethod
    def __parse_python_dict(cls, python_dict):

        container = []
        for k, v in python_dict.iteritems():
            if (isinstance(k, int) or
                isinstance(k, float)):
                key = ''.join(['[', str(k), ']'])
                value = cls.__parse_python_value(v)
                container.append(''.join([key, " = ", value]))
            elif isinstance(k, str):
                key = k
                value = cls.__parse_python_value(v)
                container.append(''.join([key, " = ", value]))
        return '{' + ','.join(container) + '}'


    @classmethod
    def __parse_python_list(cls, python_list):

        container = []
        for i in python_list:
            container.append(cls.__parse_python_value(i))
        return '{' + ','.join(container) + '}'


    @classmethod
    def __parse_python_string(cls, python_string):

        # escape_convert_table = {
        #     '\a' : "\\a",  # '\a' (bell),
        #     '\b' : "\\b",  # '\b' (backspace),
        #     '\f' : "\\f",  # '\f' (form feed),
        #     '\n' : "\\n",  # '\n' (newline),
        #     '\r' : "\\r",  # '\r' (carriage return),
        #     '\t' : "\\t",  # '\t' (horizontal tab),
        #     '\v' : "\\v",  # '\v' (vertical tab),
        #     '\\' : "\\\\", # '\\' (backslash),
        #     '\"' : '\\"',  # '\"' (double quote),
        #     '\'' : "\\'",  # '\'' (single quote).
        # }
        # letter_container = []
        # for letter in python_string:
        #     if letter in escape_convert_table:
        #         letter_container.append(escape_convert_table[letter])
        #     else:
        #         letter_container.append(letter)
        # # "...\\"..."(invalid)
        # # '...\\'...'(invalid)
        # # '...\\"...\\'...'(?????)
        # string_result = ''.join(letter_container)
        # if string_result.find("'") == -1:
        #     return ''.join(["'", string_result, "'"])
        # else:
        #     return ''.join(['"', string_result, '"'])
        return "[[" + python_string + "]]"


    @classmethod
    def __parse_python_value(cls, python_value):
        if python_value is None:
            return "nil"
        elif python_value is False:
            return "false"
        elif python_value is True:
            return "true"
        elif (isinstance(python_value, int) or
              isinstance(python_value, float)):
            return str(python_value)
        elif isinstance(python_value, str):
            return cls.__parse_python_string(python_value)
        elif isinstance(python_value, list):
            return cls.__parse_python_list(python_value)
        elif isinstance(python_value, dict):
            return cls.__parse_python_dict(python_value)
        else:
            raise PythonTypeError("Python type errors!")


    @classmethod
    def __list2dict(cls, list_data):
        """convert list to dict
        """
        dict_data = {}
        index = 1
        for item in list_data:
            if isinstance(item, Pairs):
                if (not dict_data.has_key(item.first) and
                    item.second is not None):
                    dict_data[item.first] = item.second
            elif item is not None:
                dict_data[index] = item
                index += 1
        return dict_data


    @classmethod
    def __str2num(cls, num_str):
        try:
            # is int?
            num = int(num_str)
            return num
        except ValueError:
            try:
                # is float?
                num = float(num_str)
                return num
            except ValueError:
                # invalid
                return None
