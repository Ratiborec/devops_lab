import argparse
import requests

from datetime import datetime
from getpass import getpass


def get_args():

    command = argparse.ArgumentParser(description="""Get stat from Git.""")
    command.add_argument("-v", "--version",
                         action="version",
                         version='%(util)s 0.0.1')
    command.add_argument("-o", "--opened",
                         action="store_true",
                         default=False, dest="_o",
                         help="shows only opened pull requests")
    command.add_argument("-c", "--closed",
                         action="store_true",
                         default=False, dest="_c",
                         help="shows only closed pull requests")
    command.add_argument("-r", "--request",
                         dest="_r",
                         help="How many days request are opened. "
                              "You can use not full name."
                              "In this case you get all requests "
                              "which answer to your entered string")
    command.add_argument("-d", "--date",
                         dest="_d",
                         help="All requets from entered date till now.\n"
                              "Format of data Y-m-d. \n"
                              "Example:\n"
                              "python3.6 pr-stats -d 2018-07-09"
                              " [<user>] [<owner>] [<repo>]")
    command.add_argument("-f", "--filter",
                         action="store_true",
                         default=False,
                         dest="_f",
                         help="With this key you can use "
                              "additional parametrs -l, -t, -s")
    command.add_argument("-l",
                         dest="_l",
                         default="",
                         help="Login for filter")
    command.add_argument("-t",
                         dest="_t",
                         default="",
                         help="Title for filter")
    command.add_argument("-s",
                         dest="_s",
                         default="all",
                         help="State for filter")
    command.add_argument("-i", "--instuction",
                         dest="_i",
                         action="store_true",
                         default=False,
                         help="Help")

    command.add_argument(metavar="<user>",
                         type=str, dest="user",
                         help="Login to Git")
    command.add_argument(metavar='<owner>',
                         type=str, dest="owner",
                         help='Enter owner of repository')
    command.add_argument(metavar='<repo>',
                         type=str,
                         dest="repo",
                         help='Get repo from Git')

    args = command.parse_args()

    return args


class GitStat(object):

    def __init__(self, user, owner, repo):
        self.user = user
        self.password = getpass()
        self.format = '%Y-%m-%dT%H:%M:%SZ'
        self.repo = repo
        self.owner = owner
        self.req = requests.get("https://api.github.com/"
                                "repos/{0}/{1}/"
                                "pulls?page=1&per_page=1000&"
                                "state=all".format(self.owner, self.repo),
                                auth=(self.user, self.password))

    def filter(self, login="", title="", state="all"):
        """Enter name to find person and task which you want to find"""
        _tmp = []
        for i in self.req.json():
            if i["state"] == state:
                _tmp.append(i)
            elif state == "all":
                _tmp = self.req.json()

        if title == "" and login == "":
            for i in _tmp:
                print("{0:30s}{1:50s}{2:20s}".format(i["user"]["login"],
                                                     i["title"],
                                                     i["created_at"]))
        elif title == "":
            for i in _tmp:
                if login in i["user"]["login"]:
                    print("{0:30s}{1:50s}{2:20s}".format(i["user"]["login"],
                                                         i["title"],
                                                         i["created_at"]))
        elif login == "":
            for i in _tmp:
                if title in i["title"]:
                    print("{0:30s}{1:50s}{2:20s}".format(i["user"]["login"],
                                                         i["title"],
                                                         i["created_at"]))
        else:
            for i in _tmp:
                if login in i["user"]["login"] and title in i["title"]:
                    print("{0:30s}{1:50s}{2:20s}".format(i["user"]["login"],
                                                         i["title"],
                                                         i["created_at"]))
        print("-" * 50)

    def closed(self):
        """Show only closed user/title"""
        for i in self.req.json():
            if i["state"] == "closed":
                print("{0:30s}{1:50s}".format(i["user"]["login"],
                                              i["title"]))
        print("-" * 50)

    def opened(self):
        """Show only opened user/title"""
        for i in self.req.json():
            if i["state"] == "open":
                print("{0:30s}{1:50s}".format(i["user"]["login"],
                                              i["title"]))
        print("-" * 50)

    def count_opened(self, title):
        """How many days is opened"""
        if title:
            for i in self.req.json():
                if title in i["title"]:
                    date = datetime.strptime(i["created_at"],
                                             self.format)
                    days = date.now().day - date.day
                    print("{0:30s}{1:40s} "
                          "Opened: {2:5d}".
                          format(i["user"]["login"],
                                 i["title"],
                                 days))

    def from_date(self, _from):
        """All requets which are created from  ..."""
        date_from = datetime.strptime(_from, "%Y-%m-%d")
        print(date_from.date())
        for i in self.req.json():
            if datetime.strptime(i["created_at"],
                                 self.format).date() >= date_from.date():
                print("{0:30s}{1:40s} "
                      "Created at: {2:5s}".
                      format(i["user"]["login"],
                             i["title"],
                             i["created_at"]))
        print("-" * 50)


def start():
    args = get_args()
    git_obj = GitStat(args.user, args.owner, args.repo)
    if args._o:
        git_obj.opened()
    if args._c:
        git_obj.closed()
    if args._d:
        git_obj.from_date(args._d)
    if args._r:
        git_obj.count_opened(args._r)
    if args._f:
        git_obj.filter(args._l, args._t, args._s)


if __name__ == "__main__":
    start()
