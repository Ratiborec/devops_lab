
_name = input("Enter the company name: ")
_list = []

_dict = {}

for char in _name:
    if _dict.get(char) is None:
        _dict[char] = 1
    else:
        _dict[char] += 1

_sorted_values = sorted(_dict.values(), reverse=True)
_sorted_keys = sorted(_dict.keys())
_new_dict = {}
for key in _sorted_keys:
    _new_dict[key] = _dict[key]
_dict.clear()

for val in _sorted_values:
    for i in _new_dict:
        if _new_dict[i] == val:
            _dict[i] = val

print(_dict)
_out_keys = list(_dict.keys())

for i in range(3):
    print("{0}  {1}".format(_out_keys[i], _sorted_values[i]))

