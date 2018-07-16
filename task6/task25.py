def count_char(_name):
	_dict = {}
	for char in _name:
		if _dict.get(char) is None:
			_dict[char] = 1
		else:
			_dict[char] += 1
	return _dict


def sort_chars(_dict):
	if not isinstance(_dict, dict):
		return "Incorrect data"
	else:
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
		return _dict


def output(_dict):
	if not isinstance(_dict, dict):
		return "Incorrect data"
	else:
		_out_keys = list(_dict.keys())
		_sorted_values = sorted(_dict.values(), reverse=True)
		if len(_dict) == 0:
			print("Empty data")
		else:
			for i in range(len(_dict)):
				print("{0}  {1}".format(_out_keys[i], _sorted_values[i]))


if __name__ == "__main__":
	name = input("Enter the company name: ")
	_dict = sort_chars(count_char(name))
	output(_dict)
