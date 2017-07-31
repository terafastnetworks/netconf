"""Test Ports Script"""
from lib.system_config import System_Config
from lib.config import get_config_arg

sysDict = {

    'name': 'optical,polatis,switch',
    'password': 'optical,polatis,switch',
    'group': 'view,admin,user',
    'interface_status':
    get_config_arg('system_config', 'interface_status'),
    'interface':
    get_config_arg('system_config', 'interface'),
    'mode_preserve': 'MODE_PRESERVE',
    'mode_volatile': 'MODE_VOLATILE',
    'single_name': 'polatis',
    'single_password': 'polatis',
    'single_group': 'admin',
    'invalid_name_with_special_char': 'polatis@',
    'invalid_name_with_max_lim': 'polatisopticalswitches12345678933',
    'invalid_password_with_special_char': 'polatis@$',
    'invalid_password_with_max_lim': 'polatisopticalswitches12345678933',
    'invalid_group': 'administrator',
    'invalid_mode_preserve': 'MODE_PRE',
    'invalid_mode_volatile': 'MODE_VOL'


}


class test_view_system_config_opr:

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.sys_cfg = System_Config()
        cls.sys_cfg.connect_switch()

    def test_view_create_user_with_password_and_group_using_get(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(
            file_name='test_view_create_user_with_password_and_group.xml',
            names=sysDict['name'],
            passwords=sysDict['password'],
            groups=sysDict['group'], operation = 'get')

    def test_view_create_user_with_password_and_group_using_getconfig(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(
            file_name='test_view_create_user_with_password_and_group.xml',
            names=sysDict['name'],
            passwords=sysDict['password'],
            groups=sysDict['group'], operation = 'get-config')

    def test_view_create_user_with_max_limit_username(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(
            file_name='test_view_create_user_with_password_and_group.xml',
            names='wearetryingtosetmaxa',
            passwords='',
            groups=sysDict['group'].split(',')[0], operation = 'get')        

    def test_view_create_user_without_password_and_group_using_get(self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_user_without_password_and_group(
            file_name='test_view_create_user_without_password_and_group.xml',
            names=sysDict['name'], operation = 'get')
        
    def test_view_create_user_without_password_and_group_using_get_config(self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_user_without_password_and_group(
            file_name='test_view_create_user_without_password_and_group.xml',
            names=sysDict['name'], operation = 'get-config')
 
    def test_view_create_startup_mode_with_mode_preserve_using_get(self):
        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_preserve(
            file_name='test_view_create_startup_mode_with_mode_preserve.xml',
            mode_preserve=sysDict['mode_preserve'], operation = 'get')
        
    def test_view_create_startup_mode_with_mode_preserve_using_getconfig(self):
        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_preserve(
            file_name='test_view_create_startup_mode_with_mode_preserve.xml',
            mode_preserve=sysDict['mode_preserve'], operation = 'get-config')
        
    def test_view_create_startup_mode_with_mode_volatile_using_get(self):
        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_volatile(
            file_name='test_view_create_startup_mode_with_mode_volatile.xml',
            mode_volatile=sysDict['mode_volatile'], operation = 'get')

    def test_view_create_startup_mode_with_mode_volatile_using_get_config(self):
        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_volatile(
            file_name='test_view_create_startup_mode_with_mode_volatile.xml',
            mode_volatile=sysDict['mode_volatile'], operation = 'get-config')

    def test_view_create_user_with_group_and_invalid_password_with_max_limit(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_group_and_invalid_password(
            file_name='test_view_create_user_with_group_and_invalid_password_with_max_limit.xml',
            names=sysDict['single_name'],
            passwords=sysDict['invalid_name_with_max_lim'],
            groups=sysDict['single_group'])

    def test_view_create_user_with_group_and_invalid_password_with_special_char(
            self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_group_and_invalid_password(
            file_name='test_view_create_user_with_group_and_invalid_password_with_special_char.xml',
            names=sysDict['single_name'],
            passwords=sysDict['invalid_password_with_special_char'],
            groups=sysDict['single_group'])

    def test_view_create_user_with_password_and_invalid_group(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_invalid_group(
            file_name='test_view_create_user_with_password_and_invalid_group.xml',
            names=sysDict['single_name'],
            passwords=sysDict['single_password'],
            groups=sysDict['invalid_group'])

    def test_view_create_invalid_user_special_char_without_password_and_group(
            self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_invalid_user_without_password_and_group(
            file_name='test_view_create_invalid_user_special_char_without_password_and_group.xml',
            names=sysDict['invalid_name_with_special_char'])

    def test_view_create_invalid_user_max_lim_without_password_and_group(self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_invalid_user_without_password_and_group(
            file_name='test_view_create_invalid_user_max_lim_without_password_and_group.xml',
            names=sysDict['invalid_name_with_max_lim'])

    def test_view_create_invalid_startup_mode_with_mode_preserve(self):
        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_invalid_startup_mode_with_mode_preserve(
            file_name='test_view_create_invalid_startup_mode_with_mode_preserve.xml',
            mode_preserve=sysDict['invalid_mode_preserve'])

    def test_view_create_invalid_startup_mode_with_mode_volatile(self):
        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_invalid_startup_mode_with_mode_volatile(
            file_name='test_view_create_invalid_startup_mode_with_mode_volatile.xml',
            mode_volatile=sysDict['invalid_mode_volatile'])

    #def testEditConfigDeleteAllUsers(self):
    #    """ testing delete all users """
    #    self.sys_cfg.editconfig_delete_all_users(
    #        file_name='editconfig_delete_all_users.xml')

    def test_view_get_interface_status(self):
        """ testing create user without password and group """
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status.xml',
            interface_status_info=sysDict['interface_status'].split(','), subelement = 'interface-status')
        
    def test_view_get_eth0_interface_status_name_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        eth0_interface_status =[]
        for info in range(0, 6):
            eth0_interface_status.append(interface_status[info])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status_name_object.xml', interface_name = sysDict['interface_status'].split(',')[0], 
             interface_status_info = eth0_interface_status, subelement = 'name')
        
    def test_view_get_eth0_interface_status_ip_address_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface_status'].split(',')
        eth0_interface_status = []
        eth0_interface_status.append(sysDict['interface_status'].split(',')[0])
        eth0_interface_status.append(sysDict['interface_status'].split(',')[1])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status_ip_address_object.xml',
            interface_name=sysDict['interface_status'].split(',')[0], interface_status_info = eth0_interface_status,subelement = 'ip-address')
        
    def test_view_get_eth0_interface_status_gateway_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface_status'].split(',')
        eth0_interface_status = []
        eth0_interface_status.append(sysDict['interface_status'].split(',')[0])
        eth0_interface_status.append(sysDict['interface_status'].split(',')[2])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status_gateway_object.xml',
            interface_name=sysDict['interface_status'].split(',')[0], interface_status_info = eth0_interface_status, subelement = 'gateway')
        
    def test_view_get_eth0_interface_status_subnet_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface_status'].split(',')
        eth0_interface_status = []
        eth0_interface_status.append(sysDict['interface_status'].split(',')[0])
        eth0_interface_status.append(sysDict['interface_status'].split(',')[3])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status_subnet_object.xml',
            interface_name=sysDict['interface_status'].split(',')[0], interface_status_info = eth0_interface_status, subelement = 'subnet')
        
    def test_view_get_eth0_interface_status_broadcast_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface_status'].split(',')
        eth0_interface_status = []
        eth0_interface_status.append(sysDict['interface_status'].split(',')[0])
        eth0_interface_status.append(sysDict['interface_status'].split(',')[4])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_status_broadcast_object.xml',
            interface_name=sysDict['interface_status'].split(',')[0], interface_status_info = eth0_interface_status, subelement = 'broadcast')
        
    def test_view_get_eth0_interface_status_hw_addr_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface_status'].split(',')
        eth0_interface_status = []
        eth0_interface_status.append(sysDict['interface_status'].split(',')[0])
        eth0_interface_status.append(sysDict['interface_status'].split(',')[5])
        self.sys_cfg.get_interface_status(
            file_name='test_view_get_interface_satus_hw_addr_object.xml',
            interface_name=sysDict['interface_status'].split(',')[0], interface_status_info = eth0_interface_status, subelement = 'hw-addr')

    def test_view_get_eth1_interface_status_name_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status =[]
            for info in range(6, 12):
                eth0_interface_status.append(interface_status[info])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_status_name_object.xml', interface_name = sysDict['interface_status'].split(',')[6], 
                 interface_status_info = eth0_interface_status, subelement = 'name')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return
        
    def test_view_get_eth1_interface_status_ip_address_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status = []
            eth0_interface_status.append(sysDict['interface_status'].split(',')[6])
            eth0_interface_status.append(sysDict['interface_status'].split(',')[7])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_status_ip_address_object.xml',
                interface_name=sysDict['interface_status'].split(',')[6], interface_status_info = eth0_interface_status,subelement = 'ip-address')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return
        
    def test_view_get_eth1_interface_status_gateway_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status = []
            eth0_interface_status.append(sysDict['interface_status'].split(',')[6])
            eth0_interface_status.append(sysDict['interface_status'].split(',')[8])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_status_gateway_object.xml',
                interface_name=sysDict['interface_status'].split(',')[6], interface_status_info = eth0_interface_status, subelement = 'gateway')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return
        
    def test_view_get_eth1_interface_status_subnet_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status = []
            eth0_interface_status.append(sysDict['interface_status'].split(',')[6])
            eth0_interface_status.append(sysDict['interface_status'].split(',')[9])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_status_subnet_object.xml',
                interface_name=sysDict['interface_status'].split(',')[6], interface_status_info = eth0_interface_status, subelement = 'subnet')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return
        
    def test_view_get_eth1_interface_status_broadcast_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status = []
            eth0_interface_status.append(sysDict['interface_status'].split(',')[6])
            eth0_interface_status.append(sysDict['interface_status'].split(',')[10])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_status_broadcast_object.xml',
                interface_name=sysDict['interface_status'].split(',')[6], interface_status_info = eth0_interface_status, subelement = 'broadcast')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return
        
    def test_view_get_eth1_interface_status_hw_addr_object(self):
        """ testing create user without password and group """
        interface_status = sysDict['interface_status'].split(',')
        if len(interface_status) > 6:
            eth0_interface_status = []
            eth0_interface_status.append(sysDict['interface_status'].split(',')[6])
            eth0_interface_status.append(sysDict['interface_status'].split(',')[11])
            self.sys_cfg.get_interface_status(
                file_name='test_view_get_interface_satus_hw_addr_object.xml',
                interface_name=sysDict['interface_status'].split(',')[6], interface_status_info = eth0_interface_status, subelement = 'hw-addr')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return


    def test_view_get_interface(self):
        """ testing create user without password and group """
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface.xml',
            interface_info=sysDict['interface'].split(','), subelement = 'interface')
        
    def test_view_get_eth0_interface_name_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        eth0_interface =[]
        for info in range(0, 5):
            eth0_interface.append(interface[info])
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface_name_object.xml', interface_name = sysDict['interface'].split(',')[0], 
             interface_info = eth0_interface, subelement = 'name')

    def test_view_get_eth0_interface_ip_address_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        eth0_interface = []
        eth0_interface.append(sysDict['interface'].split(',')[0])
        eth0_interface.append(sysDict['interface'].split(',')[1])
        
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface_ip_address_object.xml', interface_name = sysDict['interface'].split(',')[0],
             interface_info = eth0_interface, subelement = 'ip-address')

    def test_view_get_eth0_interface_gateway_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        eth0_interface = []
        eth0_interface.append(sysDict['interface'].split(',')[0])
        eth0_interface.append(sysDict['interface'].split(',')[2])
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface_gateway_object.xml', interface_name = sysDict['interface'].split(',')[0], 
            interface_info = eth0_interface , subelement = 'gateway')

    def test_view_get_eth0_interface_subnet_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        eth0_interface = []
        eth0_interface.append(sysDict['interface'].split(',')[0])
        eth0_interface.append(sysDict['interface'].split(',')[3])
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface_subnet_object.xml', interface_name = sysDict['interface'].split(',')[0],
            interface_info = eth0_interface , subelement = 'subnet')

    def test_view_get_eth0_interface_broadcast_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        eth0_interface = []
        eth0_interface.append(sysDict['interface'].split(',')[0])
        eth0_interface.append(sysDict['interface'].split(',')[4])
        self.sys_cfg.get_interface(
            file_name='test_view_get_interface_broadcast_object.xml', interface_name = sysDict['interface'].split(',')[0],
            interface_info = eth0_interface, subelement = 'broadcast')

    def test_view_get_eth1_interface_name_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        if len(interface) > 5:
            eth0_interface =[]
            for info in range(5, 10):
                eth0_interface.append(interface[info])
            self.sys_cfg.get_interface(
                file_name='test_view_get_interface_name_object.xml', interface_name = sysDict['interface'].split(',')[5], 
                 interface_info = eth0_interface, subelement = 'name')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return

    def test_view_get_eth1_interface_ip_address_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        if len(interface) > 5:
            eth0_interface = []
            eth0_interface.append(sysDict['interface'].split(',')[5])
            eth0_interface.append(sysDict['interface'].split(',')[6])
            
            self.sys_cfg.get_interface(
                file_name='test_view_get_interface_ip_address_object.xml', interface_name = sysDict['interface'].split(',')[5],
                 interface_info = eth0_interface, subelement = 'ip-address')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return

    def test_view_get_eth1_interface_gateway_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        if len(interface) > 5:
            eth0_interface = []
            eth0_interface.append(sysDict['interface'].split(',')[5])
            eth0_interface.append(sysDict['interface'].split(',')[7])
            self.sys_cfg.get_interface(
                file_name='test_view_get_interface_gateway_object.xml', interface_name = sysDict['interface'].split(',')[5], 
                interface_info = eth0_interface , subelement = 'gateway')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return

    def test_view_get_eth1_interface_subnet_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        if len(interface) > 5:
            eth0_interface = []
            eth0_interface.append(sysDict['interface'].split(',')[5])
            eth0_interface.append(sysDict['interface'].split(',')[8])
            self.sys_cfg.get_interface(
                file_name='test_view_get_interface_subnet_object.xml', interface_name = sysDict['interface'].split(',')[5],
                interface_info = eth0_interface , subelement = 'subnet')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return

    def test_view_get_eth1_interface_broadcast_object(self):
        """ testing create user without password and group """
        interface = sysDict['interface'].split(',')
        if len(interface) > 5:
            eth0_interface = []
            eth0_interface.append(sysDict['interface'].split(',')[5])
            eth0_interface.append(sysDict['interface'].split(',')[9])
            self.sys_cfg.get_interface(
                file_name='test_view_get_interface_broadcast_object.xml', interface_name = sysDict['interface'].split(',')[5],
                interface_info = eth0_interface, subelement = 'broadcast')
        else:
            print "INFO : eth1 interface is not supported in this switch..."
            return

    #def testGetStartupMode(self):
    #    """ testing get startup mode """
    #    self.sys_cfg.get_startup_mode(
    #        file_name='testGetStartupMode.xml',
    #        mode_volatile=sysDict['mode_volatile'])

    #def testGetConfigStartupMode(self):
    #    """ testing get startup mode """
    #    self.sys_cfg.getconfig_startup_mode(
    #        file_name='get_startup_mode.xml',
    #        mode_volatile=sysDict['mode_volatile'])

    #def testGetUserWithGroup(self):
    #    """ testing get user """
    #    self.sys_cfg.get_user_with_group(
    #        file_name='get_user.xml',
    #        names=sysDict['name'],
    #        groups=sysDict['group'],
    #        passwords=sysDict['password'])

    #def testGetConfigUserWithGroup(self):
    #    """ testing get user """
    #    self.sys_cfg.getconfig_user_with_group(
    #        file_name='get_user.xml',
    #        names=sysDict['name'],
    #        groups=sysDict['group'],
    #        passwords=sysDict['password'])

    #def testGetCurrentDatetime(self):
    #    """ testing get currrent datetime """
    #    self.sys_cfg.get_current_datetime(file_name='get_user.xml')
