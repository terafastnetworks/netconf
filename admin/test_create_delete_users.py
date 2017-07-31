"""Test Ports Script"""
from lib.system_config import System_Config
from lib.config import get_config_arg

sysDict = {

    'name': 'adm_user,usr_user,vew_user',
    'password': 'adm_user,usr_user,vew_user',
    'group': 'admin,user,view',


}


class test_system_config_opr:

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.sys_cfg = System_Config()
        cls.sys_cfg.connect_switch()

    def test_create_user_with_password_and_group_using_get(self):
        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(
            file_name='test_create_user_with_password_and_group.xml',
            names=get_config_arg('login_credentials', 'users'),
            passwords=get_config_arg('login_credentials', 'passwords'),
            groups=get_config_arg('login_credentials', 'groups'), operation = 'get')


    def test_delete_all_users(self):
        """ testing delete all users """
        self.sys_cfg.delete_all_users(
            file_name='test_delete_all_users.xml')

