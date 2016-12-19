import PyLuaTblParser

test_str1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,nil,string = "value", ignore = nil},\
            array = {3,6,4,},string = nil,},}'

test_str2 = '{array = {65,23,5,},dict = {mixed = {[66] = "ha\'ha",54.33,false,9,string = "va\nlue",},array = {3,6,4,},string = "value",}}'
test_str3 = "{1,2,3,4}"

test_dict = {'array': [65, 23, 5], 'dict': {'mixed': {1: 43, 2: 54.33, 3: False, 4: None, 'string': 'value'}, 'array': [3, 6, 4]}}
test_str4 = '{-20.123,-0x123.ef, 0Xad.efa, 20, 20.1,   ,23}'


t_string_1 = '{[[hello]], "zaijian", \'good bye\'}'

t_table_1 = '{name1 = {1,1e10, name2 = {"hehe", [[nihao]], ["key"] = "value", "hello "  ..   "world!" },}, "1"}'


print '1' * 16
a = PyLuaTblParser.PyLuaTblParser(test_str1)
print a.lua_table_dict
print '*' * 32
a.loadDict(test_dict)
print a.dump()
b = PyLuaTblParser.PyLuaTblParser(a.dump())
print b.lua_table_dict

print '*' * 32
print '*' * 32
print '*' * 32
a.load(t_table_1)
print a.lua_table_dict



# b = PyLuaTblParser.PyLuaTblParser(test_str1)
# c = PyLuaTblParser.PyLuaTblParser(test_str2)
# d = PyLuaTblParser.PyLuaTblParser(test_str4)
# a.loadDict(c.dumpDict())
# c.dumpLuaTable("/Users/loosen/Program/python/python/luatable")
# b.loadLuaTable("/Users/loosen/Program/python/python/luatable")
# hehe = a.update(test_dict)
# hehe_str = a.dump()
# print hehe_str

# print a.lua_table_dict
# # print b.lua_table_dict
# print c.lua_table_str
# print "*" * 16
# print a.dump()

# print "+" * 16
# print id(a.lua_table_dict)
# print id(c.lua_table_dict)

# print c.lua_table_dict == a.lua_table_dict

# print "--" * 16
# print c.lua_table_str
# print b.lua_table_str
# print c.lua_table_dict == b.lua_table_dict
# print d.lua_table_dict


#  42-->load
#  372-->__parse_lua_basic_exp
#  223-->__parse_lua_table
#  332-->__parse_lua_table
#  385-->
