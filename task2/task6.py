def normal_mask(_list):
    for i in _list:
        for oct in range(4):
            if len(i[oct]) < 8:
                if len(i[oct]) == 0:
                    i[oct] = "00000000" + i[oct]
                elif len(i[oct]) == 1:
                    i[oct] = "0000000" + i[oct]
                elif len(i[oct]) == 2:
                    i[oct] = "000000" + i[oct]
                elif len(i[oct]) == 3:
                    i[oct] = "00000" + i[oct]
                elif len(i[oct]) == 4:
                    i[oct] = "0000" + i[oct]
                elif len(i[oct]) == 5:
                    i[oct] = "000" + i[oct]
                elif len(i[oct]) == 6:
                    i[oct] = "00" + i[oct]
                elif len(i[oct]) == 7:
                    i[oct] = "0" + i[oct]
    return _list


_netmask = input("Enter through the space netmasks: ")
_netmask = _netmask.split(" ")

_file = open("INPUT.txt", "w")
_file.write(str(len(_netmask)) + "\n")
for i in _netmask:
    _file.write(i + "\n")

_count = int(input("Enter count of paitrs of IP:"))
_file.write(str(_count) + "\n")


for i in range(_count):
    print("Enter pair IP through the space:")
    _file.write(input() + "\n")
_file.close()


_file = open("INPUT.txt", "r")
_count_netmask = _file.readline()
_list_netmask = []
_list_ip = []


for i in range(int(_count_netmask)):
    _tmp_list = _file.readline().split(".")
    for j in range(4):
        _tmp_list[j] = bin(int(_tmp_list[j]))[2:]
    _list_netmask.append(_tmp_list)


_count_ip_pairs = _file.readline()
for i in range(int(_count_ip_pairs)):
    _tmp_list = _file.readline().split(" ")
    _tmp_list[0] = _tmp_list[0].split(".")
    _tmp_list[1] = _tmp_list[1].split(".")
    for j in range(4):
        _tmp_list[0][j] = bin(int(_tmp_list[0][j]))[2:]
        _tmp_list[1][j] = bin(int(_tmp_list[1][j]))[2:]
    _list_ip.append(_tmp_list)
_file.close()


for col in _list_ip:
    for count in range(2):
        for i in col[count]:
            for oct in range(4):
                if len(col[count][oct]) < 8:
                    if len(col[count][oct]) == 0:
                        col[count][oct] = "00000000" + col[count][oct]
                    elif len(col[count][oct]) == 1:
                        col[count][oct] = "0000000" + col[count][oct]
                    elif len(col[count][oct]) == 2:
                        col[count][oct] = "000000" + col[count][oct]
                    elif len(col[count][oct]) == 3:
                        col[count][oct] = "00000" + col[count][oct]
                    elif len(col[count][oct]) == 4:
                        col[count][oct] = "0000" + col[count][oct]
                    elif len(col[count][oct]) == 5:
                        col[count][oct] = "000" + col[count][oct]
                    elif len(col[count][oct]) == 6:
                        col[count][oct] = "00" + col[count][oct]
                    elif len(col[count][oct]) == 7:
                        col[count][oct] = "0" + col[count][oct]


_list_netmask = normal_mask(_list_netmask)


_int_mask = []
for mask in range(int(_count_netmask)):
    _tmp = _list_netmask[mask]
    _int_mask.append(str("".join(_tmp)))

_int_ip = []
for pair in range(int(_count_ip_pairs)):
    for ip in _list_ip[pair]:
        _int_ip.append(str("".join(ip)))

_counter = 0
for ip in range(0, int(len(_int_ip)), 2):
    for mask in _int_mask:
        _ip1 = _int_ip[ip]
        _ip2 = _int_ip[ip + 1]
        _inc = 0
        while mask[_inc] == '1':
            if _ip1[_inc] != _ip2[_inc]:
                break
            _inc += 1
        else:
            _counter += 1
    _file = open("OUTPUT.txt", "a")
    _file.write(str(_counter) + "\n")
    _file.close()
    _counter = 0
