import psutil
import subprocess
import time


def cpu():
    """cpu load"""
    cpu_load = psutil.cpu_percent(interval=1)
    return cpu_load


def virtual_memory():
    """virtual_memory"""
    virt_mem = psutil.virtual_memory()
    return (virt_mem.used / (1024 * 1024 * 1024))


def io_information():
    """IO information"""
    io_info = psutil.disk_io_counters(perdisk=False)
    return io_info


def disk_info():
    """Disk usage"""
    disk = psutil.disk_usage("/")
    return (disk.used / (1024 * 1024 * 1024))


def network_info():
    """Networks"""
    netstat = psutil.net_io_counters(pernic=False, nowrap=True)
    return netstat


def network_adapter_info():
    """Network adapter info"""
    net_adapter = psutil.net_if_addrs()
    return net_adapter


def organization_txt(_cpu_load, _virt_mem_used, _io, _disk, _network, _adap):
    """making output txt file"""
    p1 = "load {0}, virt: {1},read: {read}, write: {write}, " \
         "busy: {busy}," \
         " disk: {disk}, ".format(_cpu_load, _virt_mem_used,
                                  read=_io.read_count, write=_io.write_count,
                                  busy=_io.busy_time, disk=_disk)
    p2 = "ip: {ip}, mask: {mask}," \
         " recv: {recv}," \
         " sent: {sent} " \
         "".format(ip=_adap["em1"][0].address,
                   mask=_adap["em1"][0].netmask,
                   recv=_network.bytes_recv,
                   sent=_network.bytes_sent)
    p1 += p2
    return p1


def organization_json(_cpu_load, _virt_mem, _io, _disk, _network, _adap):
    """making output json file"""
    json_out = {}
    json_out["cpu"] = _cpu_load
    json_out["virt_mem"] = _virt_mem
    json_out["disk"] = _disk
    json_out["io"] = {"read": _io.read_count,
                      "write": _io.write_count,
                      "busy": _io.busy_time}
    json_out["adapter"] = {"ip": _adap["em1"][0].address,
                           "mask": _adap["em1"][0].netmask}
    json_out["network"] = {"recv": _network.bytes_recv,
                           "sent": _network.bytes_sent}
    return json_out


def read_config():
    json = {}
    json["interval"] = 1
    json["output"] = "json"
    file = open("config.ini", "r")
    while True:
        summary = file.readline().rstrip("\n")
        if summary == "[config]":
            while True:
                line = file.readline().rstrip("\n")
                params = line.split(" ")
                if line == "":
                    break
                elif params[0] == "interval":
                    json["interval"] = int(params[2])
                elif params[0] == "output":
                    json["output"] = params[2]
        elif summary == "":
            break
    file.close()

    return json


def check_num_txt():
    check = ""
    for line in reversed(open("log.txt", "r").readlines()):
        check = line
        break
    if check == "":
        return 1
    else:
        check = check.split(":")
        num = int(check[0][9:])
        num += 1
        return num


def check_num_json():
    check = ""
    for line in reversed(open("log.json", "r").readlines()):
        check = line
        break
    if check == "":
        return 1
    else:
        check = check.split(",")
        num = int(check[0][13:]) + 1
        return num


def write_log():
    _params = read_config()
    if _params["output"] == "json":
        _dict = {}
        _json = organization_json(cpu(),
                                  virtual_memory(),
                                  io_information(),
                                  disk_info(),
                                  network_info(),
                                  network_adapter_info())
        file = open("log.json", "a")
        i = check_num_json()
        _dict["SNAPSHOT"] = i
        _dict["time"] = time.ctime()
        _dict["log"] = _json
        file.write("{0}\n".format(_dict))
        file.close()
    if _params["output"] == "txt":
        _txt = organization_txt(cpu(),
                                virtual_memory(),
                                io_information(),
                                disk_info(),
                                network_info(),
                                network_adapter_info())
        file = open("log.txt", "a")
        file.write("SNAPSHOT"
                   " {i}:{t}:{j}\n"
                   "".format(t=time.ctime(),
                             i=check_num_txt(),
                             j=_txt))
        file.close()


def start():
    config = read_config()
    interval = int(config["interval"])
    file = open("crontab.txt", "w")
    file.write(str(interval) + " * * * * /usr/"
                               "bin/python36 "
                               "/home/student/"
                               "PycharmProjects/"
                               "task3/task1.py\n")
    file.close()
    params = ["/usr/bin/crontab", "/home/"
                                  "student/"
                                  "PycharmProjects/"
                                  "task3/crontab.txt"]
    subprocess.Popen(params)


if __name__ == "__main__":
    write_log()
