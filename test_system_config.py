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


class test_system_config_opr:

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.sys_cfg = System_Config()
        cls.sys_cfg.connect_switch()

    def testEditConfigCreateUserWithPasswordAndGroup(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(
            file_name='editconfig_create_user_with_pw_grp.xml',
            names=sysDict['name'],
            passwords=sysDict['password'],
            groups=sysDict['group'])

    def testEditConfigCreateUserWithoutPasswordAndGroup(self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_user_without_password_and_group(
            file_name='editconfig_create_user_without_pw_grp.xml',
            names=sysDict['name'])

    def testEditConfigCreateStartupModeWithModePreserve(self):
        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_preserve(
            file_name='get_startup_mode_with_mode_preserve.xml',
            mode_preserve=sysDict['mode_preserve'])

    def testEditConfigCreateStartupModeWithModeVolatile(self):
        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_volatile(
            file_name='get_startup_mode_with_mode_volatile.xml',
            mode_volatile=sysDict['mode_volatile'])

    def testEditConfigCreateUserWithGroupAndInvalidPasswordWithMaxLim(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_group_and_invalid_password(
            file_name='editconfig_create_user_with_group_and_invalid_password.xml',
            names=sysDict['single_name'],
            passwords=sysDict['invalid_name_with_max_lim'],
            groups=sysDict['single_group'])

    def testEditConfigCreateUserWithGroupAndInvalidPasswordWithSpecialChar(
            self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_group_and_invalid_password(
            file_name='editconfig_create_user_with_group_and_invalid_password.xml',
            names=sysDict['single_name'],
            passwords=sysDict['invalid_password_with_special_char'],
            groups=sysDict['single_group'])

    def testEditConfigCreateUserWithPasswordAndInvalidGroup(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_invalid_group(
            file_name='editconfig_create_user_with_password_and_invalid_group.xml',
            names=sysDict['single_name'],
            passwords=sysDict['single_password'],
            groups=sysDict['invalid_group'])

    def testEditConfigCreateInvalidUserSpecialCharWithoutPasswordAndGroup(
            self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_invalid_user_without_password_and_group(
            file_name='editconfig_create_invalid_user_without_password_and_group.xml',
            names=sysDict['invalid_name_with_special_char'])

    def testEditConfigCreateInvalidUserMaxLimWithoutPasswordAndGroup(self):
        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_invalid_user_without_password_and_group(
            file_name='editconfig_create_invalid_user_without_password_and_group.xml',
            names=sysDict['invalid_name_with_max_lim'])

    def testEditConfigCreateInvalidStartupModeWithModePreserve(self):
        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_invalid_startup_mode_with_mode_preserve(
            file_name='get_startup_mode_with_mode_preserve.xml',
            mode_preserve=sysDict['invalid_mode_preserve'])

    def testEditConfigCreateInvalidStartupModeWithModeVolatile(self):
        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_invalid_startup_mode_with_mode_volatile(
            file_name='get_startup_mode_with_mode_volatile.xml',
            mode_volatile=sysDict['invalid_mode_volatile'])

    def testEditConfigDeleteAllUsers(self):
        """ testing delete all users """
        self.sys_cfg.editconfig_delete_all_users(
            file_name='editconfig_delete_all_users.xml')

    def testGetInterfaceStatus(self):
        """ testing create user without password and group """
        self.sys_cfg.get_interface_status(
            file_name='get_interface_status.xml',
            interface_status=sysDict['interface_status'])

    def testGetInterface(self):
        """ testing create user without password and group """
        self.sys_cfg.get_interface(
            file_name='get_interface.xml',
            interface=sysDict['interface'])

    def testGetStartupMode(self):
        """ testing get startup mode """
        self.sys_cfg.get_startup_mode(
            file_name='get_startup_mode.xml',
            mode_volatile=sysDict['mode_volatile'])

    def testGetConfigStartupMode(self):
        """ testing get startup mode """
        self.sys_cfg.getconfig_startup_mode(
            file_name='get_startup_mode.xml',
            mode_volatile=sysDict['mode_volatile'])

    def testGetUserWithGroup(self):
        """ testing get user """
        self.sys_cfg.get_user_with_group(
            file_name='get_user.xml',
            names=sysDict['name'],
            groups=sysDict['group'],
            passwords=sysDict['password'])

    def testGetConfigUserWithGroup(self):
        """ testing get user """
        self.sys_cfg.getconfig_user_with_group(
            file_name='get_user.xml',
            names=sysDict['name'],
            groups=sysDict['group'],
            passwords=sysDict['password'])

    def testGetCurrentDatetime(self):
        """ testing get currrent datetime """
        self.sys_cfg.get_current_datetime(file_name='get_user.xml')
