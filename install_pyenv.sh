#!/bin/bash
yum install vim git  gcc gcc-c++ make patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel -y

curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

cat ~/.bash_profile | grep pyenv > /dev/nul
if [ $? -ne 0 ]
then 
	echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bash_profile
	echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
	echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
fi

export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

yum install -y python-virtualenv

pyenv install 2.7
pyenv install 3.5.0
pyenv virtualenv 2.7 py2
pyenv virtualenv 3.5.0 py3

