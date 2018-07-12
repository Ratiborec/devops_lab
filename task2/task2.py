def write_to_file(_name, _first, _second):
    file = open(_name, "w")
    _first = str(_first)
    _second = str(_second)
    file.write(_first + "\n")
    file.write(_second)
    file.close()


def read_from_file(_name):
    file = open(_name, "r")
    _from_file = file.readlines()
    file.close()

    i = len(_from_file)
    while i > 0:
        _from_file[i - 1] = _from_file[i - 1].strip("\n")
        i -= 1
    return _from_file


def make_digit_gretter(_num):
    _tmp_list = []
    _tmp_num = " ".join(str(_num))
    for i in _tmp_num[::2]:
        _tmp_list.append(i)
    _tmp_list.sort(reverse=True)
    _num = int("".join(_tmp_list))
    return _num


def make_digit_less(_num):
    _tmp_list = []
    _tmp_num = " ".join(str(_num))
    for i in _tmp_num[::2]:
        _tmp_list.append(i)
    _tmp_list.sort()
    _num = int("".join(_tmp_list))
    return _num


_in = input("Enter income value: ")
_out = input("Enter expenditure value: ")
write_to_file("INPUT.txt", _in, _out)
data = read_from_file("INPUT.txt")

_in = int(data[0])
_out = int(data[1])
_tmp_in = 0
if _in > 0:
    _tmp_in = make_digit_gretter(_in)
elif _in < 0:
    _tmp_in = make_digit_less(abs(_in)) * (-1)


if _out > 0:
    _tmp_out = make_digit_less(_out)
elif _out < 0:
    _tmp_out = make_digit_gretter(abs(_out)) * (-1)

write_to_file("OUTPUT.txt", _tmp_in - _out, _in - _tmp_out)
print(read_from_file("OUTPUT.txt"))
