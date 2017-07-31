"""Test Ports Script"""
from lib.ports import Ports
from lib.config import get_config_arg
from lib.get_switch_ports_info_from_ports_range import get_valid_ports


portsDict = {

    'port_ids': get_valid_ports(),
    'port_label': 'port1,port2,port3',
    'replace_port_label': 'polatis1,polatis2,polatis3',
    'enable_port_state': 'PC_ENABLED,PC_ENABLED,PC_ENABLED',
    'disable_port_state': 'PC_DISABLED,PC_DISABLED,PC_DISABLED',
    'enable_port_status': 'PO_ENABLED,PO_ENABLED,PO_ENABLED',
    'disable_port_status': 'PO_DISABLED,PO_DISABLED,PO_DISABLED',
    'lambda': '1400.0,1400.0,1400.0',
    'power_high_alarm': '25.0,10.0,25.0',
    'power_low_alarm': '-60.0,-20.0,-60.0',
    'power_high_warning_offset': '25.0,25.0,15.0',
    'power_low_warning_offset': '10.0,20.0,30.0',
    'power_alarm_control':
    'POWER_ALARM_DISABLED,POWER_ALARM_CONTINUOUS,POWER_ALARM_SINGLE',
    'power_alarm_status':
    'POWER_ALARM_STATUS_OFF,POWER_ALARM_STATUS_ARMED,POWER_ALARM_STATUS_ARMED',
    'offset': '0.5,0.2,0.4',
    'averaging_time_select': '1,4,7',
    'power_alarm_hysteresis': '1.0,3.0,5.0',
    'power_alarm_clear_holdoff': '60,60,60',
    'opm_values' : '1550.0,25.0,-59.98,0.0,0.0,POWER_ALARM_DISABLED,0.0,4,10',
    'opm_val' : '10.0,POWER_ALARM_SINGLE',
    'opm_v' : '-10.0,POWER_ALARM_CONTINUOUS',

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
    'invalid_power_high_warning_offset': '100.0',
    'invalid_power_low_warning_offset': '-70.00',
    'invalid_power_alarm_control': 'POWER_ALARM_DISBLED',
    'invalid_power_alrm_control': 'INVALID_POWER_ALARM_DISABLED',
    'invalid_power_alarm_status': 'POWER_ALARM_STATUS',
    'invalid_offset': '300.0',
    'invalid_averaging_time_select': '200',
    'invalid_power_alarm_hysteresis': '200.0',
    'invalid_power_alarm_clear_holdoff': '4200',
    'invalid_opm_values' : '1800.0,100.0,-100,0.0,0.0,POWER_ALARM_DISABLD,1000.0,14,1000',
    'invalid_opm_value' : '1800.0,100.0,-100,0.0,0.0,POWER_ALARM_DISABLED,1000.0,1,1000',
    'invalid_opm_val' : '100, POWER_ALARM_DISBLED'
}


class test_admin_ports_opr():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.oxc = Ports()
        cls.oxc.connect_switch()

    def test_admin_create_port_label_and_validate_with_get(self):
        """ testing create port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_create_port_lable_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get', opr = 'create')
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get', opr = 'delete')

    def test_admin_create_port_label_and_validate_with_getconfig(self):
        """ testing create port label  and validate with getconfig"""
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_create_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get-config', opr = 'create')
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get-config', opr = 'delete')

    def test_admin_get_port_label_for_single_port(self):
        """ testing create port label  and validate with getconfig"""
        self.oxc.editconfig_create_port_label('single',
            file_name='test_admin_get_port_label_for_single_port.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get-config', opr = 'create')
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get-config', opr = 'delete')

    
    def test_admin_delete_port_label_and_validate_with_get(self):
        """ testing delete port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get', opr = 'delete')

    def test_admin_delete_port_label_and_validate_with_getconfig(self):
        """ testing delete port label and validate with getconfig"""
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get-config', opr = 'delete')
    
    def test_admin_replace_port_label_and_validate_with_get(self):
        """ testing replace port label and validate with get"""
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_replace_port_lable_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['port_label'], operation = 'get', opr = 'replace')
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get', opr = 'delete')
        

    def test_admin_replace_port_label_and_validate_with_getconfig(self):
        """ testing replace port label and validate with getconfig  """
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_replace_port_label_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_labels=portsDict['replace_port_label'], operation = 'get-config', opr = 'replace')
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_delete_port_lable_label_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_labels=',,', operation = 'get-config', opr = 'delete')
        

    def test_admin_create_invalid_port_label_using_above_max_limit(self):
        """ testing create invalid port label using above max limit """
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_create_invalid_port_label_using_above_max_limit.xml',
            port_ids=portsDict['port_id'],
            port_labels=portsDict['invalid_port_label_with_max_lim'], operation = 'get', opr = 'create')

    def test_admin_create_invalid_port_label_using_special_char(self):
        """ testing create port label uisng special character """
        self.oxc.editconfig_create_port_label(
            file_name='test_admin_create_invalid_port_label_using_special_char.xml',
            port_ids=portsDict['port_id'],
            port_labels=portsDict['invalid_port_label_with_special_char'], operation = 'get', opr = 'create')

    def test_admin_set_invalid_port_state_using_numbers(self):
        """ testing set invalid port state using numbers """
        self.oxc.editconfig_create_invalid_port_state(
            file_name='test_admin_set_invalid_port_state_using_numbers.xml',
            port_ids=portsDict['port_id'],
            port_states=portsDict['invalid_port_state_with_numbers'], operation = 'get', opr = 'create' , msg = '\"%s\" is an invalid value.' % portsDict['invalid_port_state_with_numbers'])

    def test_admin_set_invalid_port_state_using_special_char(self):
        """ testing set invalid port state using special character """
        self.oxc.editconfig_create_invalid_port_state(
            file_name='test_admin_set_invalid_port_state_using_special_char.xml',
            port_ids=portsDict['port_id'],
            port_states=portsDict['invalid_port_state_with_special_char'], operation = 'get', opr = 'create', msg = '\"%s\" is an invalid value.' % portsDict['invalid_port_state_with_special_char'])
  
    def test_admin_enable_port_state_and_validate_with_get(self):
        """ testing enable port state and validate with get """
        self.oxc.get_port_state(
            file_name='test_admin_enable_port_state_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], operation = 'get', opr = 'create')

    def test_admin_enable_port_state_and_validate_with_getconfig(self):
        """ testing enable port state and validate with getconfig """
        self.oxc.get_port_state(
            file_name='test_admin_enable_port_state_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], operation = 'get-config', opr = 'create')

    def test_admin_disable_port_state_and_validate_with_get(self):
        """ testing disable port state and validate with get """
        self.oxc.get_port_state(
            file_name='test_admin_disable_port_state_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], operation = 'get', opr = 'create')

    def test_admin_disable_port_state_and_validate_with_getconfig(self):
        """ testing disable port state and validate with getconfig """
        self.oxc.get_port_state(
            file_name='test_admin_disable_port_state_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], operation = 'get-config', opr = 'create')

    def test_admin_enable_port_state_and_validate_with_get_port_status(self):
        """ testing enable port state and validate with get port status """
        self.oxc.get_port_status(
            file_name='test_admin_enable_port_state_and_validate_with_port_status.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['enable_port_state'], port_status=portsDict['enable_port_status'], operation = 'get', opr = 'create')

    def test_admin_disable_port_state_and_validate_with_get_port_status(self):
        """ testing disable port state and validate with get port status """
        self.oxc.get_port_state(
            file_name='test_admin_disable_port_state_and_validate_with_port_status.xml',
            port_ids=portsDict['port_ids'],
            port_states=portsDict['disable_port_state'], port_status=portsDict['disable_port_status'], operation = 'get', opr = 'create')

class test_admin_opm_opr():

    @classmethod
    def setUpClass(cls):
        """conecting switch"""
        cls.oxc = Ports()
        cls.oxc.connect_switch()

    def test_admin_set_lambda_and_validate_with_get(self):
        """ testing set lambda and valdate with get """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_set_lambda_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get', opr = 'create')

    def test_admin_set_lambda_and_validate_with_getconfig(self):
        """ testing set lambda and valdate with get config """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_set_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_lambda_and_validate_with_getconfig(self):
        """ testing set invalid lambda and validate with get config """
        self.oxc.editconfig_create_invalid_lambda(
            file_name='test_admin_set_invalid_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_id'],
            lambdas=portsDict['invalid_lambda'], opr = 'create')

    def test_admin_delete_lambda_and_validate_with_get(self):
        """ testing delete lambda and valdate with get """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_delete_lambda_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get', opr = 'delete')

    def test_admin_delete_lambda_and_validate_with_getconfig(self):
        """ testing delete lambda and valdate with get config """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_delete_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_lambda_and_validate_with_getconfig(self):
        """ testing delete invalid lambda and validate with get config """
        self.oxc.editconfig_create_invalid_lambda(
            file_name='test_admin_delete_invalid_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_id'],
            lambdas=portsDict['invalid_lambda'], opr = 'delete')

    def test_admin_remove_lambda_and_validate_with_get(self):
        """ testing remove lambda and valdate with get """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_remove_lambda_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get', opr = 'remove')

    def test_admin_remove_lambda_and_validate_with_getconfig(self):
        """ testing remove lambda and valdate with get config """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_remove_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_lambda_and_validate_with_getconfig(self):
        """ testing remove invalid lambda and validate with get config """
        self.oxc.editconfig_create_invalid_lambda(
            file_name='test_admin_remove_invalid_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_id'],
            lambdas=portsDict['invalid_lambda'], opr = 'remove')

    def test_admin_replace_lambda_and_validate_with_get(self):
        """ testing replace lambda and valdate with get """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_replace_lambda_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get', opr = 'replace')

    def test_admin_replace_lambda_and_validate_with_getconfig(self):
        """ testing replace lambda and valdate with get config """
        self.oxc.editconfig_create_lambda(
            file_name='test_admin_replace_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_ids'],
            lambdas=portsDict['lambda'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_lambda_and_validate_with_getconfig(self):
        """ testing replace invalid lambda and validate with get config """
        self.oxc.editconfig_create_invalid_lambda(
            file_name='test_admin_replace_invalid_lambda_and_validate_with_getconfig.xml',
            port_ids=portsDict['port_id'],
            lambdas=portsDict['invalid_lambda'], opr = 'replace')

    def test_admin_set_high_power_alarm_and_validate_with_get(self):
        """ testing admin set high power alarm and validate with get """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_set_high_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get', opr = 'create')

    def test_admin_set_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin set high power alarm and validate with get config """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_set_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid high power alarm with get config"""
        self.oxc.editconfig_create_invalid_power_high_alarm(
            file_name='test_admin_set_invalid_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_alarms=portsDict['invalid_power_high_alarm'], opr = 'create')

    def test_admin_delete_high_power_alarm_and_validate_with_get(self):
        """ testing admin delete high power alarm and validate with get """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_delete_high_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get', opr = 'delete')

    def test_admin_delete_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin delete high power alarm and validate with get config """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_delete_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin delete invalid high power alarm with get config"""
        self.oxc.editconfig_create_invalid_power_high_alarm(
            file_name='test_admin_delete_invalid_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_alarms=portsDict['invalid_power_high_alarm'], opr = 'delete')

    def test_admin_remove_high_power_alarm_and_validate_with_get(self):
        """ testing admin remove high power alarm and validate with get """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_remove_high_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get', opr = 'remove')

    def test_admin_remove_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin remove high power alarm and validate with get config """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_remove_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin remove invalid high power alarm with get config"""
        self.oxc.editconfig_create_invalid_power_high_alarm(
            file_name='test_admin_remove_invalid_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_alarms=portsDict['invalid_power_high_alarm'], opr = 'remove')

    def test_admin_replace_high_power_alarm_and_validate_with_get(self):
        """ testing admin replace high power alarm and validate with get """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_replace_high_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get', opr = 'replace')

    def test_admin_replace_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin replace high power alarm and validate with get config """
        self.oxc.editconfig_create_power_high_alarm(
            file_name='test_admin_replace_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_alarms=portsDict['power_high_alarm'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_high_power_alarm_and_validate_with_get_config(self):
        """ testing admin replace invalid high power alarm with get config"""
        self.oxc.editconfig_create_invalid_power_high_alarm(
            file_name='test_admin_replace_invalid_high_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_alarms=portsDict['invalid_power_high_alarm'], opr = 'replace')


    def test_admin_set_low_power_alarm_and_validate_with_get(self):
        """ testing admin set low power alarm with get """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_set_low_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get', opr = 'create')

    def test_admin_set_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin set low power alarm with get config """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_set_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid lowpower alarm with get config """
        self.oxc.editconfig_create_invalid_power_low_alarm(
            file_name='test_admin_set_invalid_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['invalid_power_low_alarm'], operation = 'get_config', opr = 'create')

    def test_admin_delete_low_power_alarm_and_validate_with_get(self):
        """ testing admin delete low power alarm with get """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_delete_low_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get', opr = 'delete')

    def test_admin_delete_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin delete low power alarm with get config """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_delete_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin delete invalid lowpower alarm with get config """
        self.oxc.editconfig_create_invalid_power_low_alarm(
            file_name='test_admin_delete_invalid_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['invalid_power_low_alarm'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_low_power_alarm_and_validate_with_get(self):
        """ testing admin remove low power alarm with get """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_remove_low_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get', opr = 'remove')

    def test_admin_remove_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin remove low power alarm with get config """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_remove_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin remove invalid lowpower alarm with get config """
        self.oxc.editconfig_create_invalid_power_low_alarm(
            file_name='test_admin_remove_invalid_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['invalid_power_low_alarm'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_low_power_alarm_and_validate_with_get(self):
        """ testing admin replace low power alarm with get """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_replace_low_power_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get', opr = 'replace')

    def test_admin_replace_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin replace low power alarm with get config """
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_replace_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_low_power_alarm_and_validate_with_get_config(self):
        """ testing admin replace invalid low power alarm with get config """
        self.oxc.editconfig_create_invalid_power_low_alarm(
            file_name='test_admin_replace_invalid_low_power_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['invalid_power_low_alarm'], operation = 'get_config', opr = 'replace')


    def test_admin_set_power_high_warning_offset_and_validate_with_get(self):
        """ testing admin set power high warning offset with get """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_set_power_high_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get', opr = 'create')

    def test_admin_set_power_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin set power high warning offset with get config """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_set_power_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin set invalid high warning offset with get config """
        self.oxc.editconfig_create_invalid_power_high_warning_offset(
            file_name='test_admin_set_invalid_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_warning_offsets=portsDict['invalid_power_high_warning_offset'], operation = 'get_config', opr = 'create')

    def test_admin_delete_power_high_warning_offset_and_validate_with_get(self):
        """ testing admin delete power high warning offset with get """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_delete_power_high_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get', opr = 'delete')

    def test_admin_delete_power_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin delete power high warning offset with get config """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_delete_power_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin delete invalid high warning offset with get config """
        self.oxc.editconfig_create_invalid_power_high_warning_offset(
            file_name='test_admin_delete_invalid_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_warning_offsets=portsDict['invalid_power_high_warning_offset'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_power_high_warning_offset_and_validate_with_get(self):
        """ testing admin remove power high warning offset with get """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_remove_power_high_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get', opr = 'remove')

    def test_admin_remove_power_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin remove power high warning offset with get config """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_remove_power_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin remove invalid high warning offset with get config """
        self.oxc.editconfig_create_invalid_power_high_warning_offset(
            file_name='test_admin_remove_invalid_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_warning_offsets=portsDict['invalid_power_high_warning_offset'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_power_high_warning_offset_and_validate_with_get(self):
        """ testing admin replace power high warning offset with get """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_replace_power_high_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get', opr = 'replace')

    def test_admin_replace_power_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin replace power high warning offset with get config """
        self.oxc.editconfig_create_power_high_warning_offset(
            file_name='test_admin_replace_power_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_high_warning_offsets=portsDict['power_high_warning_offset'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_high_warning_offset_and_validate_with_get_config(self):
        """ testing admin replace invalid high warning offset with get config """
        self.oxc.editconfig_create_invalid_power_high_warning_offset(
            file_name='test_admin_replace_invalid_high_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_high_warning_offsets=portsDict['invalid_power_high_warning_offset'], operation = 'get_config', opr = 'replace')

    def test_admin_set_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin set power low warning offset with get """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_set_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get', opr = 'create')

    def test_admin_set_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin set power low warning offset with get config """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_set_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin set invalid power low warning offset operation """
        self.oxc.editconfig_create_invalid_power_low_warning_offset(
            file_name='test_admin_set_invalid_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'], operation = 'get_config', opr = 'create')

    def test_admin_delete_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin delete power low warning offset with get """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_delete_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get', opr = 'delete')

    def test_admin_delete_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin delete power low warning offset with get config """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_delete_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin delete invalid power low warning offset operation """
        self.oxc.editconfig_create_invalid_power_low_warning_offset(
            file_name='test_admin_delete_invalid_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin remove power low warning offset with get """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_remove_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get', opr = 'remove')

    def test_admin_remove_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin remove power low warning offset with get config """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_remove_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin remove invalid power low warning offset operation """
        self.oxc.editconfig_create_invalid_power_low_warning_offset(
            file_name='test_admin_remove_invalid_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'], operation = 'get_config', opr = 'remove')
 
    def test_admin_replace_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin replace power low warning offset with get """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_replace_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get', opr = 'replace')

    def test_admin_replace_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin replace power low warning offset with get config """
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_replace_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin replace invalid power low warning offset operation """
        self.oxc.editconfig_create_invalid_power_low_warning_offset(
            file_name='test_admin_replace_invalid_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'], operation = 'get_config', opr = 'replace')

    def test_admin_set_power_alarm_control_and_validate_with_get(self):
        """ testing admin set power alarm control operation with get """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_set_power_alarm_control_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get', opr = 'create')

    def test_admin_set_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin set power alarm control operation with get config """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_set_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin set invalid power alarm control operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_set_invalid_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alarm_control'], operation = 'get_config', opr = 'create')

    def test_admin_delete_power_alarm_control_and_validate_with_get(self):
        """ testing admin delete power alarm control operation with get """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_delete_power_alarm_control_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get', opr = 'delete')

    def test_admin_delete_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin delete power alarm control operation with get config """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_delete_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin delete invalid power alarm control operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_delete_invalid_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alrm_control'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_power_alarm_control_and_validate_with_get(self):
        """ testing admin remove power alarm control operation with get """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_remove_power_alarm_control_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get', opr = 'remove')

    def test_admin_remove_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin remove power alarm control operation with get config """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_remove_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin remove invalid power alarm control operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_remove_invalid_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alrm_control'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_power_alarm_control_and_validate_with_get(self):
        """ testing admin replace power alarm control operation with get """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_replace_power_alarm_control_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get', opr = 'replace')

    def test_admin_replace_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin replace power alarm control operation with get config """
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_replace_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_power_alarm_control_and_validate_with_get_config(self):
        """ testing admin replace invalid power alarm control operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_replace_invalid_power_alarm_control_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alrm_control'], operation = 'get_config', opr = 'replace')

    def test_admin_set_offset_and_validate_with_get(self):
        """ testing admin set offset operation with get """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_set_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get', opr = 'create')

    def test_admin_set_offset_and_validate_with_get_config(self):
        """ testing admin set offset operation with get config """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_set_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_offset_and_validate_with_get_config(self):
        """ testing admin set invalid offset operation with get config """
        self.oxc.editconfig_create_invalid_offset(
            file_name='test_admin_set_invalid_offset_and_validate_with_get_config',
            port_ids=portsDict['port_id'],
            offsets=portsDict['invalid_offset'], operation = 'get_config', opr = 'create')

    def test_admin_delete_offset_and_validate_with_get(self):
        """ testing admin delete offset operation with get """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_delete_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get', opr = 'delete')

    def test_admin_delete_offset_and_validate_with_get_config(self):
        """ testing admin delete offset operation with get config """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_delete_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_offset_and_validate_with_get_config(self):
        """ testing admin delete invalid offset operation with get config """
        self.oxc.editconfig_create_invalid_offset(
            file_name='test_admin_delete_invalid_offset_and_validate_with_get_config',
            port_ids=portsDict['port_id'],
            offsets=portsDict['invalid_offset'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_offset_and_validate_with_get(self):
        """ testing admin remove offset operation with get """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_remove_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get', opr = 'remove')

    def test_admin_remove_offset_and_validate_with_get_config(self):
        """ testing admin remove offset operation with get config """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_remove_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_offset_and_validate_with_get_config(self):
        """ testing admin remove invalid offset operation with get config """
        self.oxc.editconfig_create_invalid_offset(
            file_name='test_admin_remove_invalid_offset_and_validate_with_get_config',
            port_ids=portsDict['port_id'],
            offsets=portsDict['invalid_offset'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_offset_and_validate_with_get(self):
        """ testing admin replace offset operation with get """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_replace_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get', opr = 'replace')

    def test_admin_replace_offset_and_validate_with_get_config(self):
        """ testing admin replace offset operation with get config """
        self.oxc.editconfig_create_offset(
            file_name='test_admin_replace_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            offsets=portsDict['offset'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_offset_and_validate_with_get_config(self):
        """ testing admin replace invalid offset operation with get config """
        self.oxc.editconfig_create_invalid_offset(
            file_name='test_admin_replace_invalid_offset_and_validate_with_get_config',
            port_ids=portsDict['port_id'],
            offsets=portsDict['invalid_offset'], operation = 'get_config', opr = 'replace')

    def test_admin_set_averaging_time_and_validate_with_get(self):
        """ testing admin set averaging time select operation with get """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_set_averaging_time_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get', opr = 'create')

    def test_admin_set_averaging_time_and_validate_with_get_config(self):
        """ testing admin set averaging time select operation with get config """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_set_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_averaging_time_and_validate_with_get_config(self):
        """ testing admin set invalid averaging time select operation with get config """
        self.oxc.editconfig_create_invalid_averaging_time_select(
            file_name='test_admin_set_invalid_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            averaging_time_selects=portsDict['invalid_averaging_time_select'], operation = 'get_config', opr = 'create')

    def test_admin_delete_averaging_time_and_validate_with_get(self):
        """ testing admin delete averaging time select operation with get """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_delete_averaging_time_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get', opr = 'delete')

    def test_admin_delete_averaging_time_and_validate_with_get_config(self):
        """ testing admin delete averaging time select operation with get config """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_delete_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_averaging_time_and_validate_with_get_config(self):
        """ testing admin delete invalid averaging time select operation with get config """
        self.oxc.editconfig_create_invalid_averaging_time_select(
            file_name='test_admin_delete_invalid_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            averaging_time_selects=portsDict['invalid_averaging_time_select'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_averaging_time_and_validate_with_get(self):
        """ testing admin remove averaging time select operation with get """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_remove_averaging_time_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get', opr = 'remove')

    def test_admin_remove_averaging_time_and_validate_with_get_config(self):
        """ testing admin remove averaging time select operation with get config """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_remove_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_averaging_time_and_validate_with_get_config(self):
        """ testing admin remove invalid averaging time select operation with get config """
        self.oxc.editconfig_create_invalid_averaging_time_select(
            file_name='test_admin_remove_invalid_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            averaging_time_selects=portsDict['invalid_averaging_time_select'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_averaging_time_and_validate_with_get(self):
        """ testing admin replace averaging time select operation with get """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_replace_averaging_time_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get', opr = 'replace')

    def test_admin_replace_averaging_time_and_validate_with_get_config(self):
        """ testing admin replace averaging time select operation with get config """
        self.oxc.editconfig_create_averaging_time_select(
            file_name='test_admin_replace_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            averaging_time_selects=portsDict['averaging_time_select'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_averaging_time_and_validate_with_get_config(self):
        """ testing admin replace invalid averaging time select operation with get config """
        self.oxc.editconfig_create_invalid_averaging_time_select(
            file_name='test_admin_replace_invalid_averaging_time_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            averaging_time_selects=portsDict['invalid_averaging_time_select'], operation = 'get_config', opr = 'replace')

    def test_admin_set_power_alarm_hysteresis_and_validate_with_get(self):
        """ testing admin set power alarm hysteresis operation with get """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_set_power_alarm_hysteresis_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get', opr = 'create')

    def test_admin_set_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin set power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_set_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin set invalid power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_hysteresis(
            file_name='test_admin_set_invalid_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_hysteresis=portsDict['invalid_power_alarm_hysteresis'], operation = 'get_config', opr = 'create')

    def test_admin_delete_power_alarm_hysteresis_and_validate_with_get(self):
        """ testing admin delete power alarm hysteresis operation with get """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_delete_power_alarm_hysteresis_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get', opr = 'delete')

    def test_admin_delete_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin delete power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_delete_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin delete invalid power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_hysteresis(
            file_name='test_admin_delete_invalid_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_hysteresis=portsDict['invalid_power_alarm_hysteresis'], operation = 'get_config', opr = 'delete')

    def test_admin_remove_power_alarm_hysteresis_and_validate_with_get(self):
        """ testing admin remove power alarm hysteresis operation with get """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_remove_power_alarm_hysteresis_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get', opr = 'remove')

    def test_admin_remove_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin remove power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_remove_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin remove invalid power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_hysteresis(
            file_name='test_admin_remove_invalid_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_hysteresis=portsDict['invalid_power_alarm_hysteresis'], operation = 'get_config', opr = 'remove')

    def test_admin_replace_power_alarm_hysteresis_and_validate_with_get(self):
        """ testing admin replace power alarm hysteresis operation with get """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_replace_power_alarm_hysteresis_and_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get', opr = 'replace')

    def test_admin_replace_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin replace power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_power_alarm_hysteresis(
            file_name='test_admin_replace_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_hysteresis=portsDict['power_alarm_hysteresis'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_power_alarm_hysteresis_and_validate_with_get_config(self):
        """ testing admin replace invalid power alarm hysteresis operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_hysteresis(
            file_name='test_admin_replace_invalid_power_alarm_hysteresis_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_hysteresis=portsDict['invalid_power_alarm_hysteresis'], operation = 'get_config', opr = 'replace')

    def test_admin_set_power_alarm_clear_holdoff_validate_with_get(self):
        """ testing admin set power alarm clear holdoff operation with get """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_set_power_alarm_clear_holdoff_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get', opr = 'create')

    def test_admin_set_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin set power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_set_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get_config', opr = 'delete')

    def test_admin_set_invalid_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin set invalid power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_clear_holdoff(
            file_name='test_admin_set_invalid_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_clear_holdoff=portsDict['invalid_power_alarm_clear_holdoff'],  operation = 'get_config', opr = 'create')

    def test_admin_delete_power_alarm_clear_holdoff_validate_with_get(self):
        """ testing admin delete power alarm clear holdoff operation with get """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_delete_power_alarm_clear_holdoff_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get', opr = 'delete')

    def test_admin_delete_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin delete power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_delete_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin delete invalid power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_clear_holdoff(
            file_name='test_admin_delete_invalid_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_clear_holdoff=portsDict['invalid_power_alarm_clear_holdoff'],  operation = 'get_config', opr = 'delete')

    def test_admin_remove_power_alarm_clear_holdoff_validate_with_get(self):
        """ testing admin remove power alarm clear holdoff operation with get """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_remove_power_alarm_clear_holdoff_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get', opr = 'remove')

    def test_admin_remove_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin remove power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_remove_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin remove invalid power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_clear_holdoff(
            file_name='test_admin_remove_invalid_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_clear_holdoff=portsDict['invalid_power_alarm_clear_holdoff'],  operation = 'get_config', opr = 'remove')

    def test_admin_replace_power_alarm_clear_holdoff_validate_with_get(self):
        """ testing admin replace power alarm clear holdoff operation with get """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_replace_power_alarm_clear_holdoff_validate_with_get.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get', opr = 'replace')

    def test_admin_replace_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin replace power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(
            file_name='test_admin_replace_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            power_alarm_clear_holdoff=portsDict['power_alarm_clear_holdoff'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_power_alarm_clear_holdoff_validate_with_get_config(self):
        """ testing admin replace invalid power alarm clear holdoff operation with get config """
        self.oxc.editconfig_create_invalid_power_alarm_clear_holdoff(
            file_name='test_admin_replace_invalid_power_alarm_clear_holdoff_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_clear_holdoff=portsDict['invalid_power_alarm_clear_holdoff'],  operation = 'get_config', opr = 'replace')

    def test_admin_set_alarm_with_all_parameters_and_validate_with_get(self):
        """ testing admin set alarm with all parameters and validate with get """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_set_alarm_with_all_parameters_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get', opr = 'create')

    def test_admin_set_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin set alarm with all parameters and validate with get config """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_set_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin set invalid alarms with all parameters with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_all_parameters(
            file_name='test_admin_set_invalid_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_values'], opr = 'create')

    def test_admin_delete_alarm_with_all_parameters_and_validate_with_get(self):
        """ testing admin delete alarm with all parameters and validate with get """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_delete_alarm_with_all_parameters_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get', opr = 'delete')

    def test_admin_delete_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin delete alarm with all parameters and validate with get config """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_delete_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get_config', opr = 'delete')

    def test_admin_delete_invalid_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin delete invalid alarms with all parameters with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_all_parameters(
            file_name='test_admin_delete_invalid_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_value'], opr = 'delete')

    def test_admin_remove_alarm_with_all_parameters_and_validate_with_get(self):
        """ testing admin remove alarm with all parameters and validate with get """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_remove_alarm_with_all_parameters_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get', opr = 'remove')

    def test_admin_remove_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin remove alarm with all parameters and validate with get config """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_remove_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get_config', opr = 'remove')

    def test_admin_remove_invalid_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin remove invalid alarms with all parameters with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_all_parameters(
            file_name='test_admin_remove_invalid_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_value'], opr = 'remove')

    def test_admin_replace_alarm_with_all_parameters_and_validate_with_get(self):
        """ testing admin replace alarm with all parameters and validate with get """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_replace_alarm_with_all_parameters_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get', opr = 'replace')

    def test_admin_replace_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin replace alarm with all parameters and validate with get config """
        self.oxc.editconfig_create_alarm_with_all_parameters(
            file_name='test_admin_replace_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_values'], operation = 'get_config', opr = 'replace')

    def test_admin_replace_invalid_alarm_with_all_parameters_and_validate_with_get_config(self):
        """ testing admin replace invalid alarms with all parameters with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_all_parameters(
            file_name='test_admin_replace_invalid_alarm_with_all_parameters_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_value'], opr = 'replace')

    def test_admin_set_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get(self):
        """ testing admin set alarm with mode single and power low alarm and validate with get """
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_set_alarm_with_all_parameters_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

    def test_admin_set_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin set alarm with mode single power low alarm and validate with get config """
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_set_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid alarms with mode single and power low alarm with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_set_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'create')

    #def test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin delete alarm with mode single power low alarm and validate with get """
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #def test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete alarm with mode single power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #def test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete invalid alarms with mode single power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'delete')

    #def test_admin_remove_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin remove alarm with mode single power low alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_remove_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'remove')

    #def test_admin_remove_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove alarm with mode single power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_remove_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'remove')

    #def test_admin_remove_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove invalid alarms with mode single power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_remove_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'remove')

    #def test_admin_replace_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin replace alarm with mode single power low alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_replace_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'replace')

    #def test_admin_replace_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace alarm with mode single power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_replace_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'replace')

    #def test_admin_replace_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace invalid alarms with mode single power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
    #        file_name='test_admin_replace_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'replace')

    def test_admin_set_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get(self):
        """ testing admin set alarm with mode single and power low warning offset alarm and validate with get """
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_set_alarm_with_mode_sgle_power_low_warn_alarm__and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

    def test_admin_set_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
        """ testing admin set alarm with mode single power low warning offset alarm and validate with get config """
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_set_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid alarms with mode single and power low warning offset alarm with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm(
            file_name='test_admin_set_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'create')

    #def test_admin_delete_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin delete alarm with mode single power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm(
    #        file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #def test_admin_delete_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete alarm with mode single power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
    #        file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #def test_admin_delete_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete invalid alarms with mode single power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm(
    #        file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'delete')

    #def test_admin_remove_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin remove alarm with mode single power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
    #        file_name='test_admin_remove_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'remove')

    #def test_admin_remove_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove alarm with mode single power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
    #        file_name='test_admin_remove_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'remove')

    #def test_admin_remove_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove invalid alarms with mode single power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm(
    #        file_name='test_admin_remove_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'remove')

    #def test_admin_replace_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin replace alarm with mode single power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
    #        file_name='test_admin_replace_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'replace')

    #def test_admin_replace_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace alarm with mode single power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
    #        file_name='test_admin_replace_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'replace')

    #def test_admin_replace_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace invalid alarms with mode single power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm(
    #        file_name='test_admin_replace_invalid_alarm_with_mode_sgle_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'replace')

    def test_admin_set_alarm_with_mode_cont_power_low_alarm_and_validate_with_get(self):
        """ testing admin set alarm with mode continous and power low alarm and validate with get """
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_set_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'create')

    def test_admin_set_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin set alarm with mode continous power low alarm and validate with get config """
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_set_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid alarms with mode continous and power low alarm with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_set_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'create')

    #def test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin delete alarm with mode continous power low alarm and validate with get """
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'delete')

    #def test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete alarm with mode continous power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'delete')

    #def test_admin_delete_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete invalid alarms with mode continous power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_delete_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'delete')

    #def test_admin_remove_alarm_with_mode_cont_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin remove alarm with mode continous power low alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_remove_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'remove')

    #def test_admin_remove_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove alarm with mode continous power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_remove_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'remove')

    #def test_admin_remove_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove invalid alarms with mode continous power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_remove_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'remove')

    #def test_admin_replace_alarm_with_mode_cont_power_low_alarm_and_validate_with_get(self):
    #    """ testing admin replace alarm with mode continous power low alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_replace_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'replace')

    #def test_admin_replace_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace alarm with mode continous power low alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_replace_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'replace')

    #def test_admin_replace_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace invalid alarms with mode continous power low alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
    #        file_name='test_admin_replace_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'replace')

    def test_admin_set_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get(self):
        """ testing admin set alarm with mode continous and power low warning offset alarm and validate with get """
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_set_alarm_with_mode_cont_power_low_warn_alarm__and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'create')

    def test_admin_set_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
        """ testing admin set alarm with mode continous power low warning offset alarm and validate with get config """
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_set_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_ids'],
            all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'create')

    def test_admin_set_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
        """ testing admin set invalid alarms with mode continous and power low warning offset alarm with get config"""
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_set_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'create')

    #def test_admin_delete_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin delete alarm with mode continous power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_delete_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'delete')

    #def test_admin_delete_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete alarm with mode continous power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_delete_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'delete')

    #def test_admin_delete_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin delete invalid alarms with mode continous power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_delete_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'delete')

    #def test_admin_remove_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin remove alarm with mode continous power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_remove_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'remove')

    #def test_admin_remove_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove alarm with mode continous power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_remove_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'remove')

    #def test_admin_remove_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin remove invalid alarms with mode continous power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_remove_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'remove')

    #def test_admin_replace_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get(self):
    #    """ testing admin replace alarm with mode continous power low warning offset alarm and validate with get """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_replace_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get', opr = 'replace')

    #def test_admin_replace_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace alarm with mode continous power low warning offset alarm and validate with get config """
    #    self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_replace_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['opm_v'], operation = 'get_config', opr = 'replace')

    #def test_admin_replace_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config(self):
    #    """ testing admin replace invalid alarms with mode continous power low warning offset alarm with get config"""
    #    self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
    #        file_name='test_admin_replace_invalid_alarm_with_mode_cont_power_low_warn_alarm_and_validate_with_get_config.xml',
    #        port_ids=portsDict['port_id'],
    #        all_parameter_alarms=portsDict['invalid_opm_val'], opr = 'replace')


    #Clear alarm with mode OFF and validate with get

    def test_admin_clear_alarm_with_mode_off_and_validate_with_get(self):
	""" testing admin clear alarm with mode off and validate with get """

	#set default values for MODE and POWER LOW ALARM
	self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

	#trigger alarm for MODE SINGLE and POWER LOW ALARM
	self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
	    file_name='test_admin_clear_alarm_with_mode_off_and_validate_with_get.xml',
	    port_ids=portsDict['port_id'],
	    all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

	#clear alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_off_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with mode OFF and validate with get config

    def test_admin_clear_alarm_with_mode_off_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode off and validate with get config """

        #set default values for MODE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_off_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_off_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with mode OFF and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_off_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode off and validate with get config """

        #set default values for MODE and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_off_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_off_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

    #Clear alarm with mode SINGLE and validate with get

    def test_admin_clear_alarm_with_mode_single_and_validate_with_get(self):
        """ testing admin clear alarm with mode single and validate with get """

        #set default values for MODE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_continous_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_clear_alarm_with_mode_single_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get', opr = 'delete')

    #Clear alarm with mode SINGLE and validate with get config

    def test_admin_clear_alarm_with_mode_single_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode single and validate with getconfig """

        #set default values for MODE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_continous_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_clear_alarm_with_mode_single_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with mode SINGLE and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_single_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode single and validate with getconfig """

        #set default values for MODE 
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_continous_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE 
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_clear_invalid_alarm_with_mode_single_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alarm_control'], operation = 'get_config', opr = 'delete')

    #Clear alarm with mode CONTINOUS and validate with get

    def test_admin_clear_alarm_with_mode_continous_and_validate_with_get(self):
        """ testing admin clear alarm with mode continous and validate with get """

        #set default values for MODE 
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE SINGLE 
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_sgle_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE CONTINOUS 
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_continous_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with mode CONTINOUS and validate with get config

    def test_admin_clear_alarm_with_mode_continous_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode continous and validate with getconfig """

        #set default values for MODE
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_single_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS
        self.oxc.editconfig_create_power_alarm_control(
            file_name='test_admin_clear_alarm_with_mode_continous_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['power_alarm_control'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with mode CONTINOUS and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_continous_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode continous and validate with getconfig """

        #set default values for MODE
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_single_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS
        self.oxc.editconfig_create_invalid_power_alarm_control(
            file_name='test_admin_clear_invalid_alarm_with_mode_continous_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_alarm_controls=portsDict['invalid_power_alarm_control'], operation = 'get_config', opr = 'delete')

    #Clear alarm with POWER LOW ALARM and validate with get

    def test_admin_clear_alarm_with_power_low_alarm_and_validate_with_get(self):
        """ testing admin clear alarm with power low alarm and validate with get """

        #set default values for power low alarm
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_cont_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for POWER LOW ALARM
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_clear_alarm_with_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get', opr = 'delete')

    #Clear alarm with POWER LOW ALARM and validate with get config

    def test_admin_clear_alarm_with_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear alarm with power low alarm and validate with get config """

        #set default values for power low alarm
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_cont_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for POWER LOW ALARM
        self.oxc.editconfig_create_power_low_alarm(
            file_name='test_admin_clear_alarm_with_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['power_low_alarm'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with POWER LOW ALARM and validate with get config

    def test_admin_clear_invalid_alarm_with_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with power low alarm and validate with get config """

        #set default values for power low alarm
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_cont_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for POWER LOW ALARM
        self.oxc.editconfig_create_invalid_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_alarms=portsDict['invalid_power_low_alarm'], operation = 'get_config', opr = 'delete')

    #Clear alarm with MODE SINGLE and POWER LOW ALARM and validate with get

    def test_admin_clear_alarm_with_mode_single_power_low_alarm_and_validate_with_get(self):
        """ testing admin clear alarm with mode single and power low alarm and validate with get """

        #set default values for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_cont_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with MODE SINGLE and POWER LOW ALARM and validate with get config

    def test_admin_clear_alarm_with_mode_single_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode single and power low alarm and validate with get config"""

        #set default values for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_cont_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with MODE SINGLE and POWER LOW ALARM and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_single_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode single and power low alarm and validate with get config"""

        #set default values for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_cont_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_single_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

    #Clear alarm with MODE CONTINOUS and POWER LOW ALARM and validate with get

    def test_admin_clear_alarm_with_mode_continous_power_low_alarm_and_validate_with_get(self):
        """ testing admin clear alarm with mode continous and power low alarm and validate with get """

        #set default values for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_single_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_cont_power_low_alarm_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with MODE CONTINOUS and POWER LOW ALARM and validate with get config

    def test_admin_clear_alarm_with_mode_continous_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode continous and power low alarm and validate with get config"""

        #set default values for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_single_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_alarm_with_mode_continous_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with MODE CONTINOUS and POWER LOW ALARM and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_continous_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode continous and power low alarm and validate with get config"""

        #set default values for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_delete_invalid_alarm_with_mode_cont_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_sgle_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW ALARM
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(
            file_name='test_admin_clear_invalid_alarm_with_mode_continous_power_low_alarm_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

    #Clear alarm with POWER LOW WARNING OFFSET and validate with get

    def test_admin_clear_alarm_with_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin clear alarm with power low warning offset and validate with get """

        #set default values for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_cont_and_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_clear_alarm_with_power_low_warning_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get', opr = 'delete')

    #Clear alarm with POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_alarm_with_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin clear alarm with power low warning offset and validate with get config """

        #set default values for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_cont_and_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_power_low_warning_offset(
            file_name='test_admin_clear_alarm_with_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['power_low_warning_offset'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_invalid_alarm_with_power_low_warning_offset_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with power low warning offset and validate with get config """

        #set default values for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_invalid_alarm_with_mode_cont_and_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_power_low_warning_offset(
            file_name='test_admin_clear_invalid_alarm_with_power_low_warning_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            power_low_warning_offsets=portsDict['invalid_power_low_warning_offset'], operation = 'get_config', opr = 'delete')

    #Clear alarm with MODE SINGLE and POWER LOW WARNING OFFSET and validate with get

    def test_admin_clear_alarm_with_mode_single_power_low_warning_offset_and_validate_with_get(self):
        """ testing admin clear alarm with mode single and power low warning offset and validate with get """

        #set default values for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with MODE SINGLE and POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode single and power low warn offset and validate with get config"""

        #set default values for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_sgle_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with MODE SINGLE and POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_single_power_low_alarm_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode single and power low alarm and validate with get config"""

        #set default values for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_delete_invalid_alarm_with_mode_sgle_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_invalid_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE SINGLE and  POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_invalid_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

    #Clear alarm with MODE CONTINOUS and POWER LOW WARNING OFFSET and validate with get

    def test_admin_clear_alarm_with_mode_continous_power_low_warn_offset_and_validate_with_get(self):
        """ testing admin clear alarm with mode continous and power low warning offset and validate with get """

        #set default values for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get', opr = 'delete')

    #Clear alarm with MODE CONTINOUS and POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_alarm_with_mode_continous_power_low_warn_offset_and_validate_with_get_config(self):
        """ testing admin clear alarm with mode continous and power low warning offset and validate with get config"""

        #set default values for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_delete_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_single_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_alarm_with_mode_continous_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['opm_val'], operation = 'get_config', opr = 'delete')

    #Clear invalid alarm with MODE CONTINOUS and POWER LOW WARNING OFFSET and validate with get config

    def test_admin_clear_invalid_alarm_with_mode_continous_power_low_warn_offset_and_validate_with_get_config(self):
        """ testing admin clear invalid alarm with mode continous and power low warning offset and validate with get config"""

        #set default values for MODE CONTINOUS and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_delete_invalid_alarm_with_mode_cont_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

        #trigger alarm for MODE SINGLE and POWER LOW WARNING OFFSET
        self.oxc.editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_offset(
            file_name='test_admin_clear_invalid_alarm_with_mode_sgle_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'create')

        #clear alarm for MODE CONTINOUS and POWER LOW WARNING OFFSET 
        self.oxc.editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(
            file_name='test_admin_clear_invalid_alarm_with_mode_continous_power_low_warn_offset_and_validate_with_get_config.xml',
            port_ids=portsDict['port_id'],
            all_parameter_alarms=portsDict['invalid_opm_val'], operation = 'get_config', opr = 'delete')

