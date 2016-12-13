
import PyLuaTblParser

test_str1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,nil,string = "value",},\
            array = {3,6,4,},string = nil,},}'

test_str2 = '{array = {65,23,5,},dict = {mixed = {[2] = "haha",54.33,false,9,string = "value",},array = {3,6,4,},string = "value",}}'
test_str3 = "{1,2,3,4}"

test_dict = {'array': [65, 23, 5], 'dict': {'mixed': {1: 43, 2: 54.33, 3: False, 4: None, 'string': 'value'}, 'array': [3, 6, 4]}}
test_str4 = '{3,4,5,6,7}'


a = PyLuaTblParser.PyLuaTblParser()
b = PyLuaTblParser.PyLuaTblParser(test_str1)
c = PyLuaTblParser.PyLuaTblParser(test_str2)
d = PyLuaTblParser.PyLuaTblParser(test_str4)
a.loadDict(c.dumpDict())
c.dumpLuaTable("/Users/loosen/Program/python/python/luatable")
b.loadLuaTable("/Users/loosen/Program/python/python/luatable")
# hehe = a.update(test_dict)
# hehe_str = a.dump()
# print hehe_str

# print a.lua_table_dict
# print b.lua_table_dict
print c.lua_table_str
print "*" * 16
print a.dump()

print "+" * 16
print id(a.lua_table_dict)
print id(c.lua_table_dict)

print c.lua_table_dict == a.lua_table_dict

print "--" * 16
print c.lua_table_str
print b.lua_table_str
print c.lua_table_dict == b.lua_table_dict
# print d.lua_table_dict
