import psutil
import subprocess
import time


class CollectData:
    """Class which collect data"""
    def __init__(self, memory, io, network):
        self.memory = memory
        self.io = io
        self.network = network
        if memory:
            self.collect_memory()
        if io:
            self.collect_io()
        if network:
            self.collect_network()

    def cpu(self):
        """cpu load"""
        self.cpu_load = psutil.cpu_percent(interval=1)

    def virtual_memory(self):
        """virtual_memory"""
        self.virt_mem = psutil.virtual_memory().used / (1024 * 1024)

    def io_information(self):
        """IO information"""
        self.io_info = psutil.disk_io_counters(perdisk=False)

    def disk_info(self):
        """Disk usage"""
        self.disk = psutil.disk_usage("/").used / (1024 * 1024 * 1024)

    def network_info(self):
        """Networks"""
        self.netstat = psutil.net_io_counters(pernic=False, nowrap=True)

    def network_adapter_info(self):
        """Network adapter info"""
        self.net_adapter = psutil.net_if_addrs()

    def collect_memory(self):
        """if memory = 1 in confi.ini, than collect data"""
        self.cpu()
        self.virtual_memory()
        self.disk_info()

    def collect_io(self):
        """if io = 1 in confi.ini, than collect data"""
        self.io_information()

    def collect_network(self):
        """if network = 1 in confi.ini, than collect data"""
        self.network_info()
        self.network_adapter_info()

    def __str__(self):
        return_str = ""
        if self.memory:
            return_str += """\t\t\t\t\tMemory information
                             CPU Load: {0}
                             Virtual Memory: {1}
                             Disk usage: {disk}
                             """.format(self.cpu_load,
                                        self.virt_mem,
                                        disk=self.disk)
        if self.io:
            return_str += """IO information
                             IO Read: {read}
                             IO Write: {write}
                             IO Busy: {busy}
                             """.format(read=self.io_info.read_count,
                                        write=self.io_info.write_count,
                                        busy=self.io_info.busy_time)
        if self.network:
            return_str += """Network information
                             IP: {ip}
                             Netmask: {mask}
                             Bytes recived: {recv}
                             Bytes sent: {sent}""".\
                format(ip=self.net_adapter["em1"][0].address,
                       mask=self.net_adapter["em1"][0].netmask,
                       recv=self.netstat.bytes_recv,
                       sent=self.netstat.bytes_sent)
        return return_str


class WriteToLog:
    """Class for writting to log
       file for data from class CollectData"""
    def __init__(self):
        self.read_config()
        self.data = CollectData(self.config["memory"],
                                self.config["io"],
                                self.config["network"])

    def organization_txt(self):
        """making output txt file"""
        p1 = ""
        p2 = ""
        p3 = ""
        if self.config["memory"]:
            p1 = "load {0}, virt: {1}," \
                 " disk: {disk},".format(self.data.cpu_load,
                                         self.data.virt_mem,
                                         disk=self.data.disk)
        if self.config["io"]:
            p2 = "read: {read}, write: {write}, " \
                 "busy: {busy},".format(read=self.data.io_info.read_count,
                                        write=self.data.io_info.write_count,
                                        busy=self.data.io_info.busy_time)
        if self.config["network"]:
            p3 = "ip: {ip}, mask: {mask}," \
                 " recv: {recv}," \
                 " sent: {sent} "\
                .format(ip=self.data.net_adapter["em1"][0].address,
                        mask=self.data.net_adapter["em1"][0].netmask,
                        recv=self.data.netstat.bytes_recv,
                        sent=self.data.netstat.bytes_sent)

        return p1 + p2 + p3

    def organization_json(self):
        """making output json file"""
        json_out = {}
        if self.config["memory"]:
            json_out["cpu"] = self.data.cpu_load
            json_out["virt_mem"] = self.data.virt_mem
            json_out["disk"] = self.data.disk
        if self.config["io"]:
            json_out["io"] = {"read": self.data.io_info.read_count,
                              "write": self.data.io_info.write_count,
                              "busy": self.data.io_info.busy_time}
        if self.config["network"]:
            json_out["adapter"] = {"ip":
                                   self.data.net_adapter["em1"][0].address,
                                   "mask":
                                   self.data.net_adapter["em1"][0].netmask}
            json_out["network"] = {"recv": self.data.netstat.bytes_recv,
                                   "sent": self.data.netstat.bytes_sent}
        return json_out

    def read_config(self):
        self.config = {}
        self.config["interval"] = 1
        self.config["output"] = "json"
        _file = open("config.ini", "r")
        while True:
            summary = _file.readline().rstrip("\n")
            if summary == "[config]":
                while True:
                    line = _file.readline().rstrip("\n")
                    params = line.split(" ")
                    if line == "":
                        break
                    elif params[0] == "interval":
                        self.config["interval"] = int(params[2])
                    elif params[0] == "output":
                        self.config["output"] = params[2]
                    elif params[0] == "memory":
                        self.config["memory"] = int(params[2])
                    elif params[0] == "io":
                        self.config["io"] = int(params[2])
                    elif params[0] == "network":
                        self.config["network"] = int(params[2])
            elif summary == "":
                break
        _file.close()

    def check_num_txt(self):
        check = ""
        for line in reversed(open("log.txt", "r").readlines()):
            check = line
            break
        if check == "":
            self.txt_str_num = 1
        else:
            check = check.split(":")
            num = int(check[0][9:])
            num += 1
            self.txt_str_num = num

    def check_num_json(self):
        check = ""
        for line in reversed(open("log.json", "r").readlines()):
            check = line
            break
        if check == "":
            self.json_str_num = 1
        else:
            check = check.split(",")
            num = int(check[0][13:]) + 1
            self.json_str_num = num

    def write_log(self):
        if self.config["output"] == "json":
            _dict = {}
            _json = self.organization_json()
            _file = open("log.json", "a")
            self.check_num_json()
            _dict["SNAPSHOT"] = self.json_str_num
            _dict["time"] = time.ctime()
            _dict["log"] = _json
            _file.write("{0}\n".format(_dict))
            _file.close()
        else:
            self.config["output"] == "txt"
            _txt = self.organization_txt()
            _file = open("log.txt", "a")
            self.check_num_txt()
            _file.write("SNAPSHOT"
                        " {i}:{t}:{j}"
                        "\n".format(t=time.ctime(),
                                    i=self.txt_str_num,
                                    j=_txt))
            _file.close()

    def start(self):
        interval = int(self.config["interval"])
        _file = open("crontab.txt", "w")
        _file.write(str(interval) + " * * * * /usr/"
                                    "bin/python36 "
                                    "/home/student/"
                                    "PycharmProjects/"
                                    "task3/task1.py\n")
        _file.close()
        params = ["/usr/bin/crontab", "/home/"
                                      "student/"
                                      "PycharmProjects/"
                                      "task4/crontab.txt"]
        subprocess.Popen(params)
        self.write_log()


if __name__ == "__main__":
    test = WriteToLog()
    test.start()
