""" Test Product Information """

from lib.product_information import Product_Information
from lib.config import get_config_arg
from lib.get_switch_ports_info_from_ports_range import get_valid_ingress_port, get_valid_egress_port, get_valid_ports

product_info_dict = {

    'manufacturer':
    get_config_arg('product_information', 'manufacturer'),
    'serial_number':
    get_config_arg('product_information', 'serial_number'),
    'model_name': get_config_arg('product_information', 'model_name'),
    'software_version': get_config_arg(
        'product_information',
        'software_version'),
    'ingress_port_ids': get_valid_ingress_port(),
    'egress_port_ids': get_valid_egress_port(),
    'port_ids': get_valid_ports()

}


class test_view_product_information():

    @classmethod
    def setUpClass(cls):
        cls.Product_Information = Product_Information()
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        cls.Product_Information.connect_switch()

    def test_view_get_manufacturer(self):
        """ testing get manufacturer """

        self.Product_Information.get_manufacturer(
            manufacturer=product_info_dict['manufacturer'],
            file_name='test_view_get_manufacturer.xml')

    def test_view_get_serial_number(self):
        """ testing get serial number"""

        self.Product_Information.get_serial_number(
            serial_number=product_info_dict['serial_number'],
            file_name='test_view_get_serial_number.xml')

    def test_view_get_model_name(self):
        """ testing get model name """

        self.Product_Information.get_model_name(
            model_name=product_info_dict['model_name'],
            file_name='test_view_get_model_name.xml')

    def test_view_get_software_version(self):
        """ testing get software version """

        self.Product_Information.get_software_version(
            software_version=product_info_dict['software_version'],
            file_name='test_view_get_software_version.xml')

    def test_view_get_ingress_ports_port_type(self):
        """ testing get ingress ports port type info """

        self.Product_Information.get_ingress_ports_type_info(
            ingress_port_ids=product_info_dict['ingress_port_ids'],
            file_name='test_view_get_ingress_ports_port_type.xml')

    def test_view_get_ingress_ports_has_opm(self):
        """ testing get ingress ports has opm info """

        self.Product_Information.get_ingress_ports_has_opm_info(
            ingress_port_ids=product_info_dict['ingress_port_ids'],
            file_name='test_view_get_ingress_ports_has_opm.xml')

    def test_view_get_ingress_ports_has_oxc(self):
        """ testing get ingress ports has oxc info """

        self.Product_Information.get_ingress_ports_has_oxc_info(
            ingress_port_ids=product_info_dict['ingress_port_ids'],
            file_name='test_view_get_ingress_ports_has_oxc.xml')

    def test_view_get_egress_ports_port_type(self):
        """ testing get egress ports port type info """

        self.Product_Information.get_egress_ports_type_info(
            egress_port_ids=product_info_dict['egress_port_ids'],
            file_name='test_view_get_egress_ports_port_type.xml')

    def test_view_get_egress_ports_has_opm(self):
        """ testing get egress ports has opm info """

        self.Product_Information.get_egress_ports_has_opm_info(
            egress_port_ids=product_info_dict['egress_port_ids'],
            file_name='test_view_get_egress_ports_has_opm.xml')

    def test_view_get_egress_ports_has_oxc(self):
        """ testing get egress ports has oxc info """

        self.Product_Information.get_egress_ports_has_oxc_info(
            egress_port_ids=product_info_dict['egress_port_ids'],
            file_name='test_view_get_egress_ports_has_oxc.xml')


    def test_view_get_ingress_and_egress_ports_port_type(self):
        """ testing get ingress and egress ports port type info """

        self.Product_Information.get_ingress_and_egress_ports_type_info(
            port_ids=product_info_dict['port_ids'],
            file_name='test_view_get_ingress_and_egress_ports_port_type.xml')

    def test_view_get_ingress_and_egress_ports_has_opm(self):
        """ testing get ingress and egress ports has opm info """

        self.Product_Information.get_egress_ports_has_opm_info(
            egress_port_ids=product_info_dict['port_ids'],
            file_name='test_view_get_ingress_and_egress_ports_has_opm.xml')

    def test_view_get_ingress_and_egress_ports_has_oxc(self):
        """ testing get ingress and egress ports has oxc info """

        self.Product_Information.get_egress_ports_has_oxc_info(
            egress_port_ids=product_info_dict['port_ids'],
            file_name='test_view_get_ingress_and_egress_ports_has_oxc.xml')
