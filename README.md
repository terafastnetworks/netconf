++++++++++++++++++++++
Netconf Automation:
++++++++++++++++++++++

Installation:
********************
Make sure to run "sudo apt-get update" before installing the packages.

1. Install python(atleast Python 2.7.6)
2. Install python-nose(apt-get install python-nose)
3. Install git(apt-get install git)
4. Install python-paramiko(apt-get install python-paramiko)
5. Install python-lxml(apt-get install python-lxml)
6. Install libffi-dev(apt-get install libffi-dev)
7. Install libssl-dev(apt-get install libssl-dev)
8. Install cryptography(apt-get install python-crypto)

Commnds to invoke automation:
***************************
1. Clone the testsuite from git - https://github.com/terafastnetworks/netconf
2. Go to the directory - ~/netconf/
3. Modify the config.txt file as per your switch type(eg: IP, login username, password, OXC ports, etc)
4. Use python nosetests to run automation testsuites

nosetests command:
********************
1.  nosetests -s python_file.py
2.  nosetests -s python_file.py:class_name
3.  nosetests -s python_file.py:class_name.function_name python_file_2.py:class_name.function_name
