import PyLuaTblParser


# with open("/Users/loosen/Program/python/python/test_example.txt", 'r') as f_object:

#     l = []
#     sum = 0
#     for line in f_object:
#         sum += 1
#         number_str =  line[-4:]
#         number = int(number_str)
#         if number == 373:
#             continue
#         else:
#             letter = chr((number-107)/2)
#             l.append(letter)

# l2 = {'a', 'b', "'", '\n', 'hehe'}
# print ''.join(l2)


# test_str5 = ''.join(l)
# print test_str5




test_str1 = '{array = {65,23,5,},\
            dict = {mixed = {43,54.33,false,nil,string = "value", ignore = nil},\
            array = {3,6,4,},string = nil,},}'

test_str2 = '{array = {65,23,5,},dict = {mixed = {[66] = "ha\\"ha",54.33,false,9,string = "va\nlue",},array = {3,6,4,},string = "value",}}'
test_str3 = "{1,2,3,4}"

test_dict = {'array': [65, 23, 5], 'dict': {'mixed': {1: 43, 2: 54.33, 3: False, 4: None, 'string': 'value'}, 'array': [3, 6, 4]}}

test_str4 = '{-20.123,-0x123.ef, 0Xad.efa, 20, 20.1,   ,23}'


t_string_1 = '{[[hello]], "zaijian", \'good bye\'}'

t_table_1 = '{name1 = {1,1e10, name2 = {"hehe", [[nihao]], ["key"] = "value", "hello "  ..   "world!" },}, "1"}'

test_str = '{[99] = nil, nil, a = {nil, {}, hehe = nil, "haha", "4"}, 2, 4, nil}'


print '1' * 16
a = PyLuaTblParser.PyLuaTblParser(test_str)
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


test_str4 = '{--  \n    --fdfa\n, "hehe"}'


# test_str5 = ' {\r\nroot = {\r\n\t"Test Pattern String",\r\n\t-- {"object with 1 member" = {"array with 1 element",},},\r\n\t{["object with 1 member"] = {"array with 1 element",},},\r\n\t{},\r\n\t[99] = -42,\r\n\t[98] = {{}},\r\n\t[97] = {{},{}},\r\n\t[96] = {{}, 1, 2, nil},\r\n\t[95] = {1, 2, {["1"] = 1}},\r\n\t[94] = { {["1"]=1, ["2"]=2}, {1, ["2"]=2}, ["3"] = 3 },\r\n\ttrue,\r\n\tfalse,\r\n\tnil,\r\n\t{\r\n\t\t["integer"]= 1234567890,\r\n\t\treal=-9876.543210,\r\n\t\te= 0.123456789e-12,\r\n\t\tE= 1.234567890E+34,\r\n\t\tzero = 0,\r\n\t\tone = 1,\r\n\t\tspace = " ",\r\n\t\tquote = "end"},"hehe"}}'

test_str5 = """{root = {[96] = {{},1,2,nil},[1] = [[Test Pattern String]],[2] = {object with 1 member = {[[array with 1 element]]}},[99] = -42,[4] = true,[5] = false,{[6] = {comment = [[// /* <!-- --]],false = false,backslash = [[\\]],one = 1,quotes = [[&#34; (0x0022) %22 0x22 034 &#x22;]],zero = 0,integer = 1234567890,array = {nil,nil},# -- --> */ = [[ ]],special = [[`1~!@#$%^&*()_+-={':[,]}|;.</>?]],compact = {1,2,3,4,5,6,7},space = [[ ]],hex = [[0x01230x45670x89AB0xCDEF0xabcd0xef4A]],controls = [[\x08\x0c\n\r\t]]}}}}"""

a = PyLuaTblParser.PyLuaTblParser(test_str5)
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





