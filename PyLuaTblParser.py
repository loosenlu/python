

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
            if PyLuaTblParser.is_lua_table(self):
                pass
            else:
                raise Exception

    