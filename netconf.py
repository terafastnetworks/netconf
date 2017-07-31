"""
Executing Linux Shell commands from Python
"""
import os
import time
import sys


def admin():


    try:
        os.system("date")
        print "Running snmp_agent product information....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_product_information.xml  -s admin/test_product_information.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent ports....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_ports.xml  -s admin/test_ports.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent system configuration....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_system_config.xml  -s admin/test_system_config.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent cross connect....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_crossConnects.xml  -s admin/test_crossConnects.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent enable notifications....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_enable_notifications.xml  -s admin/test_enable_notifications.py")
        print "Wait 10 sec....\n"
	os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_current_and_boot_datetime.xml -s admin/test_current_and_boot_datetime.py")
	print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent current boot date and time....\n"
        time.sleep(5)

    except Exception as err:
        print "Error : %s" % err



def user():

    try:
        os.system("date")
        print "Running snmp_agent product information....\n"
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_create_delete_user.xml  -s admin/test_create_delete_users.py:test_system_config_opr.test_delete_all_users")
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_create_delete_user.xml  -s admin/test_create_delete_users.py:test_system_config_opr.test_create_user_with_password_and_group_using_get")
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_product_information.xml  -s user/test_product_information.py")
        print "Wait 10 sec....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_ports.xml  -s user/test_ports.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent system configuration....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_system_config.xml  -s user/test_system_config.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent cross connect....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_crossConnects.xml  -s user/test_crossConnects.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent enable notifications....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_enable_notifications.xml  -s user/test_enable_notifications.py")
        print "Wait 10 sec....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_create_delete_user.xml  -s admin/test_create_delete_users.py:test_system_config_opr.test_delete_all_users")
	time.sleep(5)
	#os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/user_nosetests_current_and_boot_datetime.xml -s user/test_current_and_boot_datetime.py")
        #print "Wait 10 sec....\n"
        #time.sleep(10)
        print "Running snmp_agent current boot date and time....\n"
        time.sleep(5)

    except Exception as err:
        print "Error : %s" % err


def view():

    try:
        os.system("date")
        print "Running snmp_agent product information....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_create_delete_user.xml  -s admin/test_create_delete_users.py:test_system_config_opr.test_create_user_with_password_and_group_using_get")
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_product_information.xml  -s view/test_product_information.py")
        print "Wait 10 sec....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_ports.xml  -s view/test_ports.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent system configuration....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_system_config.xml  -s view/test_system_config.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent cross connect....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_crossConnects.xml  -s view/test_crossConnects.py")
        print "Wait 10 sec....\n"
        time.sleep(10)
        print "Running snmp_agent enable notifications....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_enable_notifications.xml  -s view/test_enable_notifications.py")
        print "Wait 10 sec....\n"
        time.sleep(5)
        os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/admin_nosetests_create_delete_user.xml  -s admin/test_create_delete_users.py:test_system_config_opr.test_delete_all_users")
	time.sleep(5)	
	#os.system("nosetests --with-xunit --xunit-file=/home/polatis/polatis_automation/netconf/report/view_nosetests_current_and_boot_datetime.xml -s view/test_current_and_boot_datetime.py")
        #print "Wait 10 sec....\n"
        #time.sleep(10)
        print "Running snmp_agent current boot date and time....\n"
        time.sleep(5)

    except Exception as err:
        print "Error : %s" % err


if __name__ == '__main__':
    admin()
    user()
    view()

