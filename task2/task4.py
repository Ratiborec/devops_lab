import random


N = int(input("Enter count of users: "))

_file = open("INPUT.txt", "w")
_file.write(str(N)+"\n")
for i in range(N):
    _a = random.randint(1, 100)
    _b = random.randint(0, 1)
    _file.write("{0} {1}\n".format(_a, _b))
_file.close()

_file = open("INPUT.txt", "r")
data = int(_file.readline())
_building = []
for i in range(data):
    _tmp_str = _file.readline().strip("\n")
    _building.append(_tmp_str.split(" "))
_file.close()

_oldest_man = -1
_tmp_years = 0
for i in range(data):
    if int(_building[i][1]):
        if int(_building[i][0]) > _tmp_years:
            _tmp_years = int(_building[i][0])
            _oldest_man = i

_file = open("OUTPUT.txt", "w")
_file.write(str(_oldest_man))
_file.close()
