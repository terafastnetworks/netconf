""" Test Set and Get Current and Boot Datetime """

from lib.enable_notifications import Enable_Notifications
from config import get_config_arg


class test_user_enable_notifications():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.enable_notif = Enable_Notifications()
        cls.enable_notif.connect_switch()

    def test_user_notif_activity(self):
        """ testing configure notif activity """
        self.enable_notif.editconfig_notif_activity(
            notif_name="NOTIF_ACTIVITY",
            file_name='test_user_notif_port.xml')

    def test_user_notif_port_power(self):
        """ testing configure notif port power """
        self.enable_notif.editconfig_notif_port_power(
            notif_name="NOTIF_PORT_POWER",
            file_name='test_user_notif_port_power.xml')

    def test_user_notif_port_power_warn(self):
        """ testing configure notif port power warn """
        self.enable_notif.editconfig_notif_port_power_warn(
            notif_name="NOTIF_PORT_POWER_WARN",
            file_name='test_user_notif_port_power_warn.xml')

  #  def test_user_notif_port_switch(self):
  #      """ testing configure notif switch"""
  #      self.enable_notif.editconfig_notif_switch(
  #          notif_name="NOTIF_SWITCH",
  #          file_name='test_user_notif_port_switch.xml')

    def test_user_notif_system(self):
        """ testing configure notif system """
        self.enable_notif.editconfig_notif_system(
            notif_name="NOTIF_SYSTEM",
            file_name='test_user_notif_system.xml')

    def test_user_all_notif(self):
        """ testing configure notif system """
	enab = get_config_arg("enab_notif", "notif")
        self.enable_notif.editconfig_with_all_notif(
            notif_name= enab,
            file_name='test_user_all_notif.xml')

    def test_user_get_notif_activity(self):
        """ testing get notif activity """
        self.enable_notif.get_notif_activity(
            notif_name="NOTIF_ACTIVITY",
            file_name='test_user_get_notif_port.xml')

    def test_user_get_notif_port_power(self):
        """ testing get notif port power """
        self.enable_notif.get_notif_port_power(
            notif_name="NOTIF_PORT_POWER",
            file_name='test_user_get_notif_port_power.xml')

    def test_user_get_notif_port_power_warn(self):
        """ testing get notif port power warn"""
        self.enable_notif.get_notif_port_power_warn(
            notif_name="NOTIF_PORT_POWER_WARN",
            file_name='test_user_get_notif_port_power_warn.xml')

    #def test_user_get_notif_switch(self):
    #    """ testing get notif port """
    #    self.enable_notif.get_notif_switch(
    #        notif_name="NOTIF_SWITCH",
    #        file_name='test_user_get_notif_switch.xml')

    def test_user_get_notif_system(self):
        """ testing get notif system """
        self.enable_notif.get_notif_system(
            notif_name="NOTIF_SYSTEM",
            file_name='test_user_get_notif_system.xml')

    def test_user_get_all_notif(self):
        """ testing get notif system """
	enab = get_config_arg("enab_notif", "notif")	
        self.enable_notif.get_notif_system(
            notif_name= enab,
            file_name='test_user_get_all_notif.xml')

    def test_user_negative_case(self):
        """ testing get notif system """
        self.enable_notif.negative_case(
            notif_name="NOTIF_SYSTE",
            file_name='test_user_negative_case.xml')
