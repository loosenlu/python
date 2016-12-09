
import PyLuaTblParser

test_str1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,nil,string = "value",},\
            array = {3,6,4,},string = nil,},}'

test_str2 = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
test_str3 = "{1,2,3,4}"

test_dict = {'array': [65, 23, 5], 'dict': {'mixed': {1: 43, 2: 54.33, 3: False, 4: None, 'string': 'value'}, 'array': [3, 6, 4]}}

a = PyLuaTblParser.PyLuaTblParser()
b = PyLuaTblParser.PyLuaTblParser(test_str1)
c = PyLuaTblParser.PyLuaTblParser(test_str2)
d = PyLuaTblParser.PyLuaTblParser(test_str3)

hehe = a.update(test_dict)
hehe_str = a.dump()

print a.lua_table_dict
print b.lua_table_dict
print c.lua_table_dict
print d.lua_table_dict
