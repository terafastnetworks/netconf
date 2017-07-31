"""Test Ports Script"""
from lib.ports import Ports
from lib.config import get_config_arg
from lib.get_switch_ports_info_from_ports_range import get_valid_ports


portsDict = {

    'port_ids': get_valid_ports(),
    'port_label': 'port1,port2,port3',
    'replace_port_label': 'polatis1,polatis2,polatis3',
    'enable_port_state': 'PC_ENABLED,PC_ENABLED,PC_ENABLED',
    'disable_port_state': 'PC_ENABLED,PC_ENABLED,PC_ENABLED',
    'enable_port_status': 'PO_ENABLED,PO_ENABLED,PO_ENABLED',
    'disable_port_status': 'PO_ENABLED,PO_ENABLED,PO_ENABLED',
    'lambda': '1550.0,1260.0,1640.0',
    'power_high_alarm': '25.0,10.0,25.0',
    'power_low_alarm': '-60.0,-20.0,-60.0',
    'power_high_warning_offset': '25.0,25.0,15.0',
    'power_low_warning_offset': '0.0,-20.0,0.0',
    'power_alarm_control':
    'POWER_ALARM_ENABLED,POWER_ALARM_CONTINUOUS,POWER_ALARM_SINGLE',
    'power_alarm_status':
    'POWER_ALARM_STATUS_OFF,POWER_ALARM_STATUS_ARMED,POWER_ALARM_STATUS_ARMED',
    'offset': '0.0,0.0,0.0',
    'averaging_time_select': '1,4,7',
    'power_alarm_hysteresis': '1.0,3.0,5.0',
    'power_alarm_clear_holdoff': '60,360,3600',

    'port_id': '1',
    'invalid_port_label_with_max_lim':
    'portlabelusingmaximumlimit1234533',
    'invalid_port_label_with_special_char': '@portlabel$',
    'invalid_port_state_with_numbers': '1234567',
    'invalid_port_state_with_special_char': 'PC_ENBL@ED',
    'invalid_port_status': 'PO_ENABLE',
    'invalid_lambda': '-100',
    'invalid_power_high_alarm': '100',
    'invalid_power_low_alarm': '-70',
    'invalid_power_high_warning_offset': '0.0',
    'invalid_power_low_warning_offset': 'polatis',
    'invalid_power_alarm_control': 'POWER_ALARM_DISBLED',
    'invalid_power_alarm_status': 'POWER_ALARM_STATUS',
    'invalid_offset': '0.0',
    'invalid_averaging_time_select': '200',
    'invalid_power_alarm_hysteresis': '-1.0',
    'invalid_power_alarm_clear_holdoff': '4200'

}


class test_view_ports_opr():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.oxc = Ports()
        cls.oxc.connect_switch()

    def test_view_create_port_label_and_validate_with_get(self):
        """ testing create port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_view_create_port_lable_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get', opr = 'create')

    def test_view_create_port_label_and_validate_with_getconfig(self):
        """ testing create port label  and validate with getconfig"""
        self.oxc.editconfig_create_port_label(
            file_name='test_view_create_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get-config', opr = 'create')
    
    def test_view_delete_port_label_and_validate_with_get(self):
        """ testing delete port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_view_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get', opr = 'delete')

    def test_view_delete_port_label_and_validate_with_getconfig(self):
        """ testing delete port label and validate with getconfig"""
        self.oxc.editconfig_create_port_label(
            file_name='test_view_delete_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get-config', opr = 'delete')
    
    def test_view_replace_port_label_and_validate_with_get(self):
        """ testing replace port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_view_replace_port_lable_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get', opr = 'replace')
        

    def test_view_replace_port_label_and_validate_with_getconfig(self):
        """ testing replace port label and validate with getconfig  """
        self.oxc.editconfig_create_port_label(
            file_name='test_view_replace_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['replace_port_label'], operation = 'get-config', opr = 'replace')
        

    def test_view_create_invalid_port_label_using_above_max_limit(self):
        """ testing create invalid port label using above max limit """
        self.oxc.editconfig_create_invalid_port_label(
            file_name='test_view_create_invalid_port_label_using_above_max_limit.xml',
            port_ids=portsDict['port_id'],
            port_labels=portsDict['invalid_port_label_with_max_lim'], operation = 'get', opr = 'create')

    def test_view_create_invalid_port_label_using_special_char(self):
        """ testing create port label uisng special character """
        self.oxc.editconfig_create_invalid_port_label(
            file_name='test_view_create_invalid_port_label_using_special_char.xml',
            port_ids=portsDict['port_id'],
            port_labels=portsDict['invalid_port_label_with_special_char'], operation = 'get', opr = 'create')

    def test_view_set_invalid_port_state_using_numbers(self):
        """ testing set invalid port state using numbers """
        self.oxc.editconfig_create_invalid_port_state(
            file_name='test_view_set_invalid_port_state_using_numbers.xml',
            port_ids=portsDict['port_id'],
            port_states=portsDict['invalid_port_state_with_numbers'], operation = 'get', opr = 'create')

    def test_view_set_invalid_port_state_using_special_char(self):
        """ testing set invalid port state using special character """
        self.oxc.editconfig_create_invalid_port_state(
            file_name='test_view_set_invalid_port_state_using_special_char.xml',
            port_ids=portsDict['port_id'],
            port_states=portsDict['invalid_port_state_with_special_char'], operation = 'get', opr = 'create')
  
    def test_view_enable_port_state_and_validate_with_get(self):
        """ testing enable port state and validate with get """
        self.oxc.get_port_state(
            file_name='test_view_enable_port_state_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], operation = 'get', opr = 'create')

    def test_view_enable_port_state_and_validate_with_getconfig(self):
        """ testing enable port state and validate with getconfig """
        self.oxc.get_port_state(
            file_name='test_view_enable_port_state_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], operation = 'get-config', opr = 'create')

    def test_view_disable_port_state_and_validate_with_get(self):
        """ testing disable port state and validate with get """
        self.oxc.get_port_state(
            file_name='test_view_disable_port_state_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], operation = 'get', opr = 'create')

    def test_view_disable_port_state_and_validate_with_getconfig(self):
        """ testing disable port state and validate with getconfig """
        self.oxc.get_port_state(
            file_name='test_view_disable_port_state_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], operation = 'get-config', opr = 'create')

    def test_view_enable_port_state_and_validate_with_get_port_status(self):
        """ testing enable port state and validate with get port status """
        self.oxc.get_port_status(
            file_name='test_view_enable_port_state_and_validate_with_port_status.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], port_status=portsDict['enable_port_status'], operation = 'get', opr = 'create')

    def test_view_disable_port_state_and_validate_with_get_port_status(self):
        """ testing disable port state and validate with get port status """
        self.oxc.get_port_state(
            file_name='test_view_disable_port_state_and_validate_with_port_status.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], port_status=portsDict['disable_port_status'], operation = 'get', opr = 'create')

#    def testEditConfigCreateLambda(self):
#        """ testing create lambda operation """
#        self.oxc.editconfig_create_lambda(
#            file_name='editconfig_create_lamda.xml',
#            port_ids=portsDict['port_ids'],
#            lambdas=portsDict['lambda'])
#
#    def testEditConfigCreateInvalidLambda(self):
#        """ testing create invalid_lambda operation """
#        self.oxc.editconfig_create_invalid_lambda(
#            file_name='editconfig_create_invalid_lamda.xml',
#            port_ids=portsDict['port_id'],
#            lambdas=portsDict['invalid_lambda'])
#
#    def testEditConfigCreatePowerHighAlarm(self):
#        """ testing create editconfig_create_power_high_alarm operation """
#        self.oxc.editconfig_create_power_high_alarm(
#            file_name='editconfig_create_power_high_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_alarms=portsDict['power_high_alarm'])
#
#    def testEditConfigCreateInvalidPowerHighAlarm(self):
#        """ testing create editconfig_create_invalid_power_high_alarm operation """
#        self.oxc.editconfig_create_invalid_power_high_alarm(
#            file_name='editconfig_create_invalid_power_high_alarm.xml',
#            port_ids=portsDict['port_id'],
#            power_high_alarms=portsDict['invalid_power_high_alarm'])
#
#    def testEditConfigCreatePowerLowAlarm(self):
#        """ testing create power_low_alarm operation """
#        self.oxc.editconfig_create_power_low_alarm(
#            file_name='editconfig_create_power_low_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_alarms=portsDict['power_low_alarm'])
#
#    def testEditConfigCreateInvalidPowerLowAlarm(self):
#        """ testing create power_invalid_low_alarm operation """
#        self.oxc.editconfig_create_invalid_power_low_alarm(
#            file_name='editconfig_create_invalid_power_low_alarm.xml',
#            port_ids=portsDict['port_id'],
#            power_low_alarms=portsDict['invalid_power_low_alarm'])
#
#    def testEditConfigCreatePowerHighWarningOffset(self):
#        """ testing create power_high_warning_offset operation """
#        self.oxc.editconfig_create_power_high_warning_offset(
#            file_name='editconfig_create_power_high_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_warning_offsets=portsDict['power_high_warning_offset'])
#
#    def testEditConfigCreateInvalidPowerHighWarningOffset(self):
#        """ testing create power_invalid_high_warning_offset operation """
#        self.oxc.editconfig_create_invalid_power_high_warning_offset(
#            file_name='editconfig_create_power_invalid_high_warning_offset.xml',
#            port_ids=portsDict['port_id'],
#            power_high_warning_offsets=portsDict['invalid_power_high_warning_offset'])
#
#    def testEditConfigCreatePowerLowWarningOffset(self):
#        """ testing create power_low_warning_offset  operation """
#        self.oxc.editconfig_create_power_low_warning_offset(
#            file_name='editconfig_create_power_low_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_warning_offsets=portsDict['power_low_warning_offset'])
#
#    def testEditConfigCreateInvalidPowerLowWarningOffset(self):
#        """ testing create invalid_power_low_warning_offset  operation """
#        self.oxc.editconfig_create_invalid_power_low_warning_offset(
#            file_name='editconfig_create_invalid_power_low_warning_offset.xml',
#            port_ids=portsDict['port_id'],
#            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'])
#
#    def testEditConfigCreatePowerAlarmControl(self):
#        """ testing create power_alarm_control operation """
#        self.oxc.editconfig_create_power_alarm_control(
#            file_name='editconfig_create_power_alarm_control.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_controls=portsDict['power_alarm_control'])
#
#    def testEditConfigCreateInvalidPowerAlarmControl(self):
#        """ testing create invalid_power_alarm_control operation """
#        self.oxc.editconfig_create_invalid_power_alarm_control(
#            file_name='editconfig_create_invalid_power_alarm_control.xml',
#            port_ids=portsDict['port_id'],
#            power_alarm_controls=portsDict['invalid_power_alarm_control'])
#
#    def testEditConfigCreateOffset(self):
#        """ testing create offset operation """
#        self.oxc.editconfig_create_offset(
#            file_name='editconfig_create_offset.xml',
#            port_ids=portsDict['port_ids'],
#            offsets=portsDict['offset'])
#
#    def testEditConfigCreateInvalidOffset(self):
#        """ testing create invalid_offset operation """
#        self.oxc.editconfig_create_invalid_offset(
#            file_name='editconfig_create_invalid_offset.xml',
#            port_ids=portsDict['port_id'],
#            offsets=portsDict['invalid_offset'])
#
#    def testEditConfigCreateAveragingTimeSelect(self):
#        """ testing create averaging_time_select operation """
#        self.oxc.editconfig_create_averaging_time_select(
#            file_name='editconfig_create_averaging_time_select.xml',
#            port_ids=portsDict['port_ids'],
#            averaging_time_selects=portsDict['averaging_time_select'])
#
#    def testEditConfigCreateInvalidAveragingTimeSelect(self):
#        """ testing create invalid_averaging_time_select operation """
#        self.oxc.editconfig_create_invalid_averaging_time_select(
#            file_name='editconfig_create_averaging_time_select.xml',
#            port_ids=portsDict['port_id'],
#            averaging_time_selects=portsDict['invalid_averaging_time_select'])
#
#    def testEditConfigCreatePowerAlarmHysteresis(self):
#        """ testing create power_alarm_hysteresis operation """
#        self.oxc.editconfig_create_power_alarm_hysteresis(
#            file_name='editconfig_create_power_alarm_hysteresis.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'])
#
#    def testEditConfigCreateInvalidPowerAlarmHysteresis(self):
#        """ testing create invalid_power_alarm_hysteresis operation """
#        self.oxc.editconfig_create_invalid_power_alarm_hysteresis(
#            file_name='editconfig_create_invalid_power_alarm_hysteresis.xml',
#            port_ids=portsDict['port_id'],
#            power_alarm_hysteresis=portsDict['invalid_power_alarm_hysteresis'])
#
#    def testEditConfigCreatePowerAlarmClearHoldOff(self):
#        """ testing create power_alarm_clear_holdoff operation """
#        self.oxc.editconfig_create_power_alarm_clear_holdoff(
#            file_name='editconfig_create_power_alarm_clear_hold_off.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'])
#
#    def testEditConfigCreateInvalidPowerAlarmClearHoldOff(self):
#        """ testing create invalid_power_alarm_clear_holdoff operation """
#        self.oxc.editconfig_create_invalid_power_alarm_clear_holdoff(
#            file_name='editconfig_create_invalid_power_alarm_clear_hold_off.xml',
#            port_ids=portsDict['port_id'],
#            power_alarm_clear_holdoff=portsDict['invalid_power_alarm_clear_holdoff'])
#
#    def testGetLambda(self):
#        """ testing get- port lambda operation """
#        self.oxc.get_lambda(
#            file_name='get_lambda.xml',
#            port_ids=portsDict['port_ids'],
#            lambdas=portsDict['lambda'])
#
#    def testGetPowerHighAlarm(self):
#        """ testing get- power high alarm operation """
#        self.oxc.get_power_high_alarm(
#            file_name='get_power_high_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_alarms=portsDict['power_high_alarm'])
#
#    def testGetPowerLowAlarm(self):
#        """ testing get- power low alarm operation """
#        self.oxc.get_power_low_alarm(
#            file_name='get_power_low_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_alarms=portsDict['power_low_alarm'])
#
#    def testGetPowerHighWarningOffsets(self):
#        """ testing get- power high warning offest operation """
#        self.oxc.get_power_high_warning_offset(
#            file_name='get_power_high_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_warning_offsets=portsDict['power_high_warning_offset'])
#
#    def testGetPowerLowWarningOffset(self):
#        """ testing get- power low warning offset operation """
#        self.oxc.get_power_low_warning_offset(
#            file_name='get_power_low_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_warning_offsets=portsDict['power_low_warning_offset'])
#
#    def testGetPowerAlarmControl(self):
#        """ testing get- power alarm control operation """
#        self.oxc.get_power_alarm_control(
#            file_name='get_power_alarm_control.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_controls=portsDict['power_alarm_control'])
#
#    def testGetPowerAlarmStatus(self):
#        """ testing get- power alarm status operation """
#        self.oxc.get_power_alarm_status(
#            file_name='get_power_alarm_status.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_status=portsDict['power_alarm_status'])
#
#    def testGetPower(self):
#        """ testing get- power operation """
#        self.oxc.get_power(
#            file_name='get_power.xml',
#            port_ids=portsDict['port_ids'],
#            power=portsDict['power'])
#
#    def testGetOffset(self):
#        """ testing get- offset label operation """
#        self.oxc.get_offset(
#            file_name='get_offset.xml',
#            port_ids=portsDict['port_ids'],
#            offsets=portsDict['offset'])
#
#    def testGetAveragingTimeSelect(self):
#        """ testing get- averaging time select operation """
#        self.oxc.get_averaging_time_select(
#            file_name='get_averaging_time_select.xml',
#            port_ids=portsDict['port_ids'],
#            averaging_time_selects=portsDict['averaging_time_select'])
#
#    def testGetPowerAlarmHyteresis(self):
#        """ testing get- power alarm hysteresis operation """
#        self.oxc.get_power_alarm_hysteresis(
#            file_name='get_power_alarm_hysteresis.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'])
#
#    def testGetPowerAlarmClearHoldOff(self):
#        """ testing get- power alarm clear hold off operation """
#        self.oxc.get_power_alarm_clear_holdoff(
#            file_name='get_power_alarm_clear_holdoff.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'])
#
#    def testGetConfigLambda(self):
#        """ testing getconfig- port lambda operation """
#        self.oxc.getconfig_lambda(
#            file_name='getconfig_lambda.xml',
#            port_ids=portsDict['port_ids'],
#            lambdas=portsDict['lambda'])
#
#    def testGetConfigPowerHighAlarm(self):
#        """ testing getconfig- power high alarm operation """
#        self.oxc.getconfig_power_high_alarm(
#            file_name='getconfig_power_high_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_alarms=portsDict['power_high_alarm'])
#
#    def testGetConfigPowerLowAlarm(self):
#        """ testing getconfig- power low alarm operation """
#        self.oxc.getconfig_power_low_alarm(
#            file_name='getconfig_power_low_alarm.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_alarms=portsDict['power_low_alarm'])
#
#    def testGetConfigPowerHighWarningOffsets(self):
#        """ testing getconfig- power high warning offest operation """
#        self.oxc.getconfig_power_high_warning_offset(
#            file_name='getconfig_power_high_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_high_warning_offsets=portsDict['power_high_warning_offset'])
#
#    def testGetConfigPowerLowWarningOffset(self):
#        """ testing getconfig- power low warning offset operation """
#        self.oxc.getconfig_power_low_warning_offset(
#            file_name='getconfig_power_low_warning_offset.xml',
#            port_ids=portsDict['port_ids'],
#            power_low_warning_offsets=portsDict['power_low_warning_offset'])
#
#    def testGetConfigPowerAlarmControl(self):
#        """ testing getconfig- power alarm control operation """
#        self.oxc.getconfig_power_alarm_control(
#            file_name='getconfig_power_alarm_control.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_controls=portsDict['power_alarm_control'])
#
#    def testGetConfigOffset(self):
#        """ testing getconfig- offset label operation """
#        self.oxc.getconfig_offset(
#            file_name='getconfig_offset.xml',
#            port_ids=portsDict['port_ids'],
#            offsets=portsDict['offset'])
#
#    def testGetConfigAveragingTimeSelect(self):
#        """ testing getconfig- averaging time select operation """
#        self.oxc.getconfig_averaging_time_select(
#            file_name='getconfig_averaging_time_select.xml',
#            port_ids=portsDict['port_ids'],
#            averaging_time_selects=portsDict['averaging_time_select'])
#
#    def testGetConfigPowerAlarmHyteresis(self):
#        """ testing getconfig- power alarm hysteresis operation """
#        self.oxc.getconfig_power_alarm_hysteresis(
#            file_name='getconfig_power_alarm_hysteresis.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'])
#
#    def testGetConfigPowerAlarmClearHoldOff(self):
#        """ testing getconfig- power alarm clear hold off operation """
#        self.oxc.getconfig_power_alarm_clear_holdoff(
#            file_name='getconfig_power_alarm_clear_holdoff.xml',
#            port_ids=portsDict['port_ids'],
#            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'])
