

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
            self.update = True
        else:
            # check whether lua_table is a valid
            # lua table string.
            if :
                pass
            else:
                raise ValueError, "The lua table is invalid!"


    
    @staticmethod
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