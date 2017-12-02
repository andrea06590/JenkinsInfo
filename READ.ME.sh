# Prerequis Requests & PyYAML pour Python3+

cd ~
mkdir jenkinsMonitoring
wget https://pypi.python.org/packages/b0/e1/eab4fc3752e3d240468a8c0b284607899d2fbfb236a56b7377a329aa8d09/requests-2.18.4.tar.gz#md5=081412b2ef79bdc48229891af13f4d82
wget http://pyyaml.org/download/pyyaml/PyYAML-3.12.tar.gz

tar zxvf requests-2.18.4.tar.gz
cd requests-2.18.4
python3.x setup.py install
cd ..

tar zxvf PyYAML-3.12.tar.gz
cd PyYAML-3.12
python3.x setup.py install
cd ..