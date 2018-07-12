def write_to_file(_name, _first, _second=0):
    _file = open(_name, "w")
    _first = str(_first)
    if _second:
        _second = str(_second)
        _file.write(_first+"\n")
        _file.write(_second)
    else:
        _file.write(_first + "\n")
    _file.close()


def read_from_file(_name):
    _file = open(_name, "r")
    _from_file = _file.readlines()
    _file.close()

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
    _tmp_list = [i for i in str(_num)]
    _tmp_list.sort()
    _index = 0
    for i in _tmp_list:
        if i != "0":
            _index = _tmp_list.index(i)
            break

    _zero_pos = 0
    while _index != _zero_pos:
        _tmp_list.insert(_index + 1, "0")
        _zero_pos += 1

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
else:
    _tmp_in = _in


if _out > 0:
    _tmp_out = make_digit_less(_out)
elif _out < 0:
    _tmp_out = make_digit_gretter(abs(_out)) * (-1)
else:
    _tmp_out = _out

if _tmp_in - _out > _in - _tmp_out:
    write_to_file("OUTPUT.txt", _tmp_in - _out)
else:
    write_to_file("OUTPUT.txt", _in - _tmp_out)

print(read_from_file("OUTPUT.txt"))
