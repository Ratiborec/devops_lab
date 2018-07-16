import os
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
    json_format = {}
    json_format["interval"] = 1
    json_format["output"] = "json"
    read_file = open("config.ini", "r")
    while True:
        summary = read_file.readline().rstrip("\n")
        if summary == "[config]":
            while True:
                line = read_file.readline().rstrip("\n")
                params = line.split(" ")
                if line == "":
                    break
                else:
                    json_format.update({params[0]: params[2]})
        elif summary == "":
            break
    read_file.close()

    return json_format


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
        append_file = open("log.json", "a")
        i = check_num_json()
        _dict["SNAPSHOT"] = i
        _dict["time"] = time.ctime()
        _dict["log"] = _json
        append_file.write("{0}\n".format(_dict))
        append_file.close()
    if _params["output"] == "txt":
        _txt = organization_txt(cpu(),
                                virtual_memory(),
                                io_information(),
                                disk_info(),
                                network_info(),
                                network_adapter_info())
        append_file = open("log.txt", "a")
        append_file.write("SNAPSHOT"
                          " {i}:{t}:{j}\n"
                          "".format(t=time.ctime(),
                                    i=check_num_txt(),
                                    j=_txt))
        append_file.close()


def start():
    config = read_config()
    interval = int(config["interval"])
    write_file = open(os.path.join(config["home"], "crontab.txt"), "w")
    write_file.write(str(interval) + " * * * * {0} {1}\n".
                     format(config["python"],
                     os.path.join(config["home"], "task1.py")))
    write_file.close()
    params = [os.path.join(config["default"], "crontab"),
              os.path.join(config["home"], "crontab.txt")]
    subprocess.Popen(params)
    write_log()


if __name__ == "__main__":
    start()
