"""Test oxc Script"""
from lib.crossconnects import CrossConnects
from lib.config import get_config_arg
from lib.get_switch_ports_info_from_ports_range import get_valid_ingress_port
from lib.get_switch_ports_info_from_ports_range import get_valid_egress_port


oxcDict = {

    'valid_ingress_ports': get_valid_ingress_port(),
    'valid_egress_ports': get_valid_egress_port(),
    'invalid_ingress_ports': [1000,1010,1020],
    'invalid_egress_ports': [2000,2010,2020]

}


class test_view_oxc_opr:

    @classmethod
    def setUpClass(cls):
        cls.oxc = CrossConnects()
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        cls.oxc.connect_switch()
        cls.oxc.get_existing_port_list()
        #cls.oxc.cleanup_existing_connections(file_name='cleanup.xml')

    def test_view_get_oxc_for_single_ingress_port(self):
        """ testing get ingress port """
        self.oxc.get_ingress_ports(file_name='test_view_get_oxc_for_single_ingress_port.xml', ingress_ports=oxcDict['valid_ingress_ports'][0].split(','), egress_ports=oxcDict['valid_egress_ports'][0].split(','))

    def test_view_get_oxc_for_multiple_ingress_ports(self):
        """ testing get pairs """
        self.oxc.get_ingress_ports(
            file_name='test_view_get_oxc_for_multiple_ingress_ports.xml',
            ingress_ports=oxcDict['valid_ingress_ports'], egress_ports=oxcDict['valid_egress_ports'])

    def test_view_get_oxc_for_single_egress_port(self):
        """ testing get egress port """
        self.oxc.get_egress_ports(file_name='test_view_get_oxc_for_single_egress_port.xml', ingress_ports=oxcDict['valid_ingress_ports'][0].split(','),egress_ports=oxcDict['valid_egress_ports'][0].split(','))

    def test_view_get_oxc_for_multiple_egress_ports(self):
        """ testing get egress ports """
        self.oxc.get_egress_ports(
            file_name='test_view_get_oxc_for_multiple_egress_ports.xml', ingress_ports=oxcDict['valid_ingress_ports'], 
            egress_ports=oxcDict['valid_egress_ports'])
   
    def test_view_create_oxc_and_validate_with_get(self):
        """ testing editconfig_create_operation """
        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.editconfig_create_operation(
            file_name='test_view_create_oxc_and_validate_with_get.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'], operation = 'get')

    def test_view_delete_oxc_and_validate_with_get(self):
        """ testing editconfig_delete_operation """
        self.oxc.edit_config_create_oxc_without_opr(
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'])
        self.oxc.editconfig_delete_operation(
            file_name='test_view_delete_oxc_and_validate_with_get.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'], operation = 'get')

    def test_view_replace_oxc_and_validate_with_get(self):
        """ testing editconfig_replace_operation """
        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.edit_config_create_oxc_without_opr(
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'])

        egr_prts = oxcDict['valid_egress_ports']
        egress_prts = ''

        l = len(egr_prts)

        if len(egr_prts) == 8:
            for i in range(l - 1, -1, -3):
                prt = ''.join(egr_prts[i - 1] + egr_prts[i])
                if i == 1:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 11:
            for i in range(l - 1, -1, -4):
                prt = ''.join(egr_prts[i - 2] + egr_prts[i - 1] + egr_prts[i])
                if i == 2:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 5:
            for i in range(l - 1, -1, -2):
                prt = ''.join(egr_prts[i])
                if i == 0:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 1 or len(egr_prts) == 2 or len(egr_prts) == 3:
            egress_prts = oxcDict['valid_egress_ports']
        else:
            print "no of digits in each port should be same"

        self.oxc.editconfig_replace_operation(
            file_name='test_view_replace_oxc_and_validate_with_get.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=egress_prts, operation = 'get')


    def test_view_create_oxc_and_validate_with_get_config(self):
        """ testing editconfig_create_operation """
        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.editconfig_create_operation(
            file_name='test_view_create_oxc_and_validate_with_get_config.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'], operation = 'get-config')

    def test_view_delete_oxc_and_validate_with_get_config(self):
        """ testing editconfig_delete_operation """
        self.oxc.edit_config_create_oxc_without_opr(
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'])
        self.oxc.editconfig_delete_operation(
            file_name='test_view_delete_oxc_and_validate_with_get_config.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'], operation = 'get-config')

    def test_view_replace_oxc_and_validate_with_get_config(self):
        """ testing editconfig_replace_operation """
        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.edit_config_create_oxc_without_opr(
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'])

        egr_prts = oxcDict['valid_egress_ports']
        egress_prts = ''

        l = len(egr_prts)

        if len(egr_prts) == 8:
            for i in range(l - 1, -1, -3):
                prt = ''.join(egr_prts[i - 1] + egr_prts[i])
                if i == 1:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 11:
            for i in range(l - 1, -1, -4):
                prt = ''.join(egr_prts[i - 2] + egr_prts[i - 1] + egr_prts[i])
                if i == 2:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 5:
            for i in range(l - 1, -1, -2):
                prt = ''.join(egr_prts[i])
                if i == 0:
                    egress_prts = egress_prts + prt
                else:
                    egress_prts = egress_prts + prt + ','
        elif len(egr_prts) == 1 or len(egr_prts) == 2 or len(egr_prts) == 3:
            egress_prts = oxcDict['valid_egress_ports']
        else:
            print "no of digits in each port should be same"

        self.oxc.editconfig_replace_operation(
            file_name='test_view_replace_oxc_and_validate_with_get_config.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=egress_prts, operation = 'get-config')

    def test_view_create_oxc_with_invalid_ingress_ports(self):
        """ test_view_EditConfig_NegativeCase_With_IngressPort """

        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_ingress_port(
            file_name='test_view_create_oxc_with_invalid_ingress_ports.xml',
            ingress_ports=oxcDict['invalid_ingress_ports'],
            egress_ports=oxcDict['valid_egress_ports'])

    def test_view_create_oxc_with_invalid_egress_ports(self):
        """ test_view_EditConfig_NegativeCase_With_EgressPort """

        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_egress_port(
            file_name='test_view_create_oxc_with_invalid_egress_ports.xml',
            ingress_ports=oxcDict['valid_ingress_ports'],
            egress_ports=oxcDict['invalid_egress_ports'])

    def test_view_create_oxc_with_invalid_ingress_and_egress_ports(self):
        """ test_view_editconfig_negative_case_invalid_oxc_connection """

        #self.oxc.cleanup_existing_connections(file_name='cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_oxc_connection(
            file_name='test_view_create_oxc_with_invalid_ingress_and_egress_ports.xml',
            ingress_ports=oxcDict['invalid_ingress_ports'],
            egress_ports=oxcDict['invalid_egress_ports'])


    def test_view_get_oxc_for_invalid_ingress_port(self):
        """ testing get ingress port """
        self.oxc.get_oxc_using_invalid_ingress_port(
            file_name='test_view_get_oxc_for_invalid_ingress_port.xml',
            ingress_ports=str(oxcDict['invalid_ingress_ports'][0]).split(','), egress_ports=str(oxcDict['invalid_egress_ports'][0]).split(','))

    def test_view_get_oxc_for_invalid_ingress_port_using_text(self):
        """ testing get ingress port """
        self.oxc.get_oxc_using_invalid_ingress_port(
            file_name='test_view_get_oxc_for_invalid_ingress_port.xml',
            ingress_ports='polatis'.split(','), egress_ports=str(oxcDict['invalid_egress_ports'][0]).split(','))


    #def test_view_get_oxc_for_invalid_egress_port(self):
    #    """ testing get egress port """
    #    self.oxc.get_oxc_using_invalid_egress_port(
    #        file_name='test_view_get_oxc_for_invalid_egress_port.xml',
    #        ingress_ports=str(oxcDict['invalid_ingress_ports'][0]).split(','), egress_ports=str(oxcDict['invalid_egress_ports'][0]).split(','))
