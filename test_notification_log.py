""" Test Set and Get Current and Boot Datetime """

from lib.enable_notifications import Enable_Notifications


class test_enable_notifications():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.enable_notif = Enable_Notifications()
        cls.enable_notif.connect_switch()

    def testNotifPort(self):
        """ testing configure notif port """
        self.enable_notif.editconfig_notif_port(
            notif_name="NOTIF_PORT",
            file_name='edit_config_notif_port.xml')

    def testNotifPortPower(self):
        """ testing configure notif port power """
        self.enable_notif.editconfig_notif_port_power(
            notif_name="NOTIF_PORT_POWER",
            file_name='edit_config_notif_port_power.xml')

    def testNotifPortPowerWarn(self):
        """ testing configure notif port power warn """
        self.enable_notif.editconfig_notif_port_power_warn(
            notif_name="NOTIF_PORT_POWER_WARN",
            file_name='edit_config_notif_port_power_warn.xml')

    def testNotifPortSwitch(self):
        """ testing configure notif switch"""
        self.enable_notif.editconfig_notif_switch(
            notif_name="NOTIF_SWITCH",
            file_name='edit_config_notif_switch.xml')

    def testNotifSystem(self):
        """ testing configure notif system """
        self.enable_notif.editconfig_notif_system(
            notif_name="NOTIF_SYSTEM",
            file_name='edit_config_notif_system.xml')

    def testAllNotif(self):
        """ testing configure notif system """
        self.enable_notif.editconfig_with_all_notif(
            notif_name="NOTIF_PORT NOTIF_PORT_POWER NOTIF_PORT_POWER_WARN NOTIF_SWITCH NOTIF_SYSTEM",
            file_name='edit_config_notif_system.xml')

    def testGetNotifPort(self):
        """ testing get notif port """
        self.enable_notif.get_notif_port(
            notif_name="NOTIF_PORT",
            file_name='get_notif_port.xml')

    def testGetNotifPortPower(self):
        """ testing get notif port power """
        self.enable_notif.get_notif_port_power(
            notif_name="NOTIF_PORT_POWER",
            file_name='get_notif_port_power.xml')

    def testGetNotifPortPowerWarn(self):
        """ testing get notif port power warn"""
        self.enable_notif.get_notif_port_power_warn(
            notif_name="NOTIF_PORT_POWER_WARN",
            file_name='get_notif_port_power_warn.xml')

    def testGetNotifSwitch(self):
        """ testing get notif port """
        self.enable_notif.get_notif_switch(
            notif_name="NOTIF_SWITCH",
            file_name='get_notif_switch.xml')

    def testGetNotifSystem(self):
        """ testing get notif system """
        self.enable_notif.get_notif_system(
            notif_name="NOTIF_SYSTEM",
            file_name='get_notif_system.xml')

    def testGetAllNotif(self):
        """ testing get notif system """
        self.enable_notif.get_notif_system(
            notif_name="NOTIF_SYSTEM NOTIF_PORT NOTIF_PORT_POWER NOTIF_PORT_POWER_WARN NOTIF_SWITCH",
            file_name='get_notif_system.xml')

    def testNegativeCase(self):
        """ testing get notif system """
        self.enable_notif.negative_case(
            notif_name="NOTIF_SYSTE",
            file_name='get_notif_system.xml')
