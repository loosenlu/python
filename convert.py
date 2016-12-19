

with open("/Users/loosen/Program/python/python/test.loadluatable.txt", 'r') as f_object:

    l = []
    sum = 0
    for line in f_object:
        sum += 1
        number_str =  line[-4:]
        number = int(number_str)
        if number == 374:
            continue
        else:

            letter = chr((number-108)/2)
            l.append(letter)

    print '*' * 32
    print sum
    print '*' * 32
    print len(l)
    print '*' * 32
    print ''.join(l)

