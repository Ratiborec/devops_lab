import os
import pip
import sys
import yaml


def get_site_packages():
	for i in sys.path:
		if "site-packages" in i:
			return i
			break


def get_virt_env():
	return os.environ["VIRTUAL_ENV"]


def get_pip_version():
	return pip.__version__


def get_env():
	return sys.executable


def get_path():
	return sys.path[0]


def get_version():
	return "{0}.{1}".format(str(sys.version_info.major),
	                        str(sys.version_info.minor))


def get_alias():
	out = []
	alias = os.popen("pyenv versions --bare --skip-aliases "
	                 "| grep -e '[0-9].[0-9].[0-9]$'")
	for i in alias.read().split():
		out.append(i)
	alias.close()
	return out


def get_pip_path():
	get_path = os.popen("which pip")
	pip_path = get_path.read().split()[0]
	get_path.close()
	return pip_path


def get_pip_modules():
	module = os.popen("pip list")
	_tmp = module.read().split()
	out = dict(zip(_tmp[4::2], _tmp[5::2]))
	module.close()
	return out


def create_data_dict():
	out = {}
	out["path"] = get_path()
	out["version"] = get_version()
	out["site_packages"] = get_site_packages()
	out["virt"] = get_virt_env()
	out["all_versions"] = other_vesions()
	out["pip_version"] = get_pip_version()
	out["env"] = get_env()
	out["alias"] = get_alias()
	out["pip_path"] = get_pip_path()
	out["modules"] = get_pip_modules()
	return out


def write_json():
	_to_json = open("json.json", "w")
	_to_json.write("{0}".format(create_data_dict()))
	_to_json.close()


def write_yaml():
	_to_yaml = open("yaml.yaml", "w")
	_to_yaml.write("{0}".format(yaml.dump(create_data_dict(),
	                                      default_flow_style=False)))
	_to_yaml.close()


def other_vesions():
	version = [i[:3] for i in get_alias()]
	_dict = {}
	for i in version:
		command = os.popen("pyenv which python{0}".
		                   format(i)).read().rstrip("\n")
		_dict[i] = command
	return _dict


if __name__ == "__main__":
	write_yaml()
	write_json()
