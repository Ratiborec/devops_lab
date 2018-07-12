_list = []
while True:
    _action = input("Enter action: ")
    _command_list = _action.split(" ")
    if _command_list[0] == 'insert':
        _index = int(input("Input position (0-{N}): ".format(N=len(_list))))
        print(_index)
        _list.insert(_index, int(_command_list[1]))
    elif _command_list[0] == 'print':
        print(_list)
    elif _command_list[0] == 'remove':
        _list.remove(int(_command_list[1]))
    elif _command_list[0] == 'append':
        _list.append(int(_command_list[1]))
    elif _command_list[0] == 'sort':
        _list.sort()
    elif _command_list[0] == 'pop':
        _list.pop()
    elif _command_list[0] == 'reverse':
        _list.reverse()
    elif _command_list[0] == 'exit':
        exit()
