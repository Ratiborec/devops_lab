def add_null(_more, _less):
    for i in range(len(_more) - len(_less)):
        _less = "0" + _less
    return _less


_a = int(input("Enter first number: "))
_b = int(input("Enter second number: "))


_a = "{0:b}".format(_a)
_b = "{0:b}".format(_b)

if len(_a) != len(_b):
    if len(_a) > len(_b):
        _b = add_null(_a, _b)
    else:
        _a = add_null(_b, _a)
_count = 0
for i in range(len(_a)):
    if _a[i] != _b[i]:
        _count += 1

print("{0}, {1}  step = {2}".format(_a, _b, _count))
