""" ports lib """

import nose
import sys
import time
from ncclient import manager
import logging.config
import ConfigParser
import xml.dom.minidom
from xml.dom import minidom
from xml.etree.ElementTree import *
from xml.dom.minidom import parse, parseString

from config import get_config_arg
from createCsv import csvOutput

logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('polatis')

port_sub_tag = 'none'


class Enable_Notifications:

    def connect_switch(self):
        """ Connect switch.
            Arguments:
            host        : IP address.
            port        : Valid Port No.
            username    : Valid User Name.
            password    : Valid password.
            timeout     : valid switch timeout with sec
        """

        global sw_mgr

        host = get_config_arg("login_credentials", "host")
        port = get_config_arg("login_credentials", "port")
        username = get_config_arg("login_credentials", "user_name")
        password = get_config_arg("login_credentials", "password")
        timeout = get_config_arg("login_credentials", "timeout")

        LOG.info("Connecting switch <IP:Port = %s:%s>\n" % (host, port))
        sw_mgr = manager.connect_ssh(
            host=host,
            port=port,
            username=username,
            password=password,
            timeout=int(timeout),
            hostkey_verify=False)

    def create_box(self, testcase_name):
        """create box for test case name.
        Arguments:
        testcase_name	:	valid testcase name
        """

        print "\n"
        l = len(testcase_name) + 7
        start_end_session = '       +' + (l * '-') + '+       '
        middle = '| ' + '   ' + str(testcase_name) + '  ' + ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)

    def write_to_file(self, file_name, data):
        """ write the output xml from 'get' and 'get-config' rpc request
        Arguments:
            file_name    : Give any name
            data        : XML output
        """

        f = open(file_name, 'w')
        f.write(data)
        f.close()

    def prettify(self, xmlstr):
        """Used for prettify the XML output from switch.
        Arguments:
           xmlstr       : any xml string
        """

        reparsed = minidom.parseString(xmlstr)
        return reparsed.toprettyxml(indent=" ")

    def create_xml(self, tag_name):
        """create xml with given notifications and push it to edit-config
        operation, form the xml for get the configurable variables using get-config
        operation, parse this get-config output, finally compare this tags valus with
        given tags values
        """

        global xmlstr

        config = Element('config')
        enable_notifications = SubElement(
            config,
            'enable-notifications',
            {'xmlns': "http://www.polatis.com/yang/polatis-switch"})
        enable_notifications.text = tag_name

        xmlstr = tostring(config)

        print "xmlstr : ", xmlstr
        return xmlstr

    def get_parsed_values(self, xmlData, tag_name):
        """compare the data's in list.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
           tag_name                    : give valid notification tag name
        """

        p = 'PASS'
        f = 'FAIL'

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        enable_notifications = collection.getElementsByTagName(
            "enable-notifications")[0]
        # print "enable_notifications : ", enable_notifications

        tagVal = str(enable_notifications.childNodes[0].data)
        # print "tagVal :", tagVal

        LOG.info('-----[ validate notification information ]-----\n\n')

        LOG.info('parsed-' + tag_name + 's : %s' % tagVal)

        return tagVal

    def edit_config_opr(self):
        """ create required notification using edit-config rpc request.
        Arguments:
        """

        global sw_mgr
        global xmlstr

        p = 'PASS'
        f = 'FAIL'

        try:
            LOG.info("-----[ pass xml for edit-config operation ]-----\n\n")

            xmldata = sw_mgr.edit_config(target='running', config=xmlstr)
            print "\n\n"

            LOG.info(
                '-----[ edit-config - response from the switch ]-----\n\n\n%s\n\n' %
                xmldata)
            return p

        except Exception as err:
            print "\n\n"
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n' % err)
            return f

    def editconfig_notif_port(self, **kwargs):
        """create notif_port notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_notif_port')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            print "notif : ", type(kwargs['notif_name'])
            print "result: ", type(result)
            if str(kwargs['notif_name']) == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_notif_port', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_notif_port_power(self, **kwargs):
        """create notif_port_power notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_notif_port_power')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            if kwargs['notif_name'] == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_notif_port_power', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

    def editconfig_notif_port_power_warn(self, **kwargs):
        """create notif_port_power_warn notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_notif_port_power_warn')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            if kwargs['notif_name'] == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_notif_port_power_warn', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

    def editconfig_notif_switch(self, **kwargs):
        """create notif_switch notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_notif_switch')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            if kwargs['notif_name'] == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_notif_switch', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

    def editconfig_notif_system(self, **kwargs):
        """create notif_system notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_notif_system')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            if kwargs['notif_name'] == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_notif_system', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

    def editconfig_with_all_notif(self, **kwargs):
        """create notif_system notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        self.create_box('test_editconfig_with_all_notif')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])

            if kwargs['notif_name'] == result:
                LOG.info('notif_name : %s' % result)
                LOG.info('compare both notifications : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_with_all_notif', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

    def getconfig_rpc_request(self, xmlstr, file_name):
        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr                : required tag xmlstr
           file_name             : any file name
        """

        global sw_mgr

        p = 'PASS'
        f = 'FAIL'

        try:
            # print "xmstr is : \n\n%s\n" % xmlstr
            xmlData = sw_mgr.get_config(
                source='running',
                filter=('subtree',
                        xmlstr)).data_xml
            print '\n\n'

            prettyXml = self.prettify(xmlData)
            LOG.info(
                '-----[ getconfig - response from the switch ]-----\n\n\n%s\n' %
                prettyXml)

            self.write_to_file(file_name, prettyXml)
            return (xmlData, p)

        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)
            return (err, f)

    def create_xml_for_get_opr(self):
        """create xml for queried tag and parsed it, then compare parsed values
        with given values.
        """

        LOG.info('-----[ create xml for get/getconfig operation ]-----\n')

        enable_notifications = Element(
            'plts:enable-notifications',
            {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

        xmlstr = tostring(enable_notifications)
        return xmlstr

    def get_rpc_request(self, xmlstr, file_name):
        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr                : required tag xmlstr
           file_name             : any file name
        """

        p = 'PASS'
        f = 'FAIL'

        global sw_mgr

        try:
            # print "xmstr is : \n\n%s\n" % xmlstr
            xmlData = sw_mgr.get(filter=('subtree', xmlstr)).data_xml
            print '\n\n'

            prettyXml = self.prettify(xmlData)
            LOG.info(
                '-----[ get - response from the switch ]-----\n\n\n%s\n' %
                prettyXml)

            self.write_to_file(file_name, prettyXml)
            return (xmlData, p)

        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)
            return (err, f)

    def get_notif_port(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('get_notif_port_enable_notification')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                if str(kwargs['notif_name']) == result:
                    LOG.info('notif_name : %s' % result)
                    LOG.info('compare both notifications : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_notif_port', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_notif_port_power(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('get_notif_port_power_enable_notification')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                if str(kwargs['notif_name']) == result:
                    LOG.info('notif_name : %s' % result)
                    LOG.info('compare both notifications : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'get_notif_port_power_enable_notification',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_notif_port_power_warn(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('get_notif_port_power_warn_enable_notification')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                if str(kwargs['notif_name']) == result:
                    LOG.info('notif_name : %s' % result)
                    LOG.info('compare both notifications : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_notif_port_power_warn', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_notif_switch(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('get_notif_switch')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                if str(kwargs['notif_name']) == result:
                    LOG.info('notif_name : %s' % result)
                    LOG.info('compare both notifications : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'get_notif_switch_enable_notification',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_notif_system(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('get_notif_system_enable_notification')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                if str(kwargs['notif_name']) == result:
                    LOG.info('notif_name : %s' % result)
                    LOG.info('compare both notifications : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_notif_system', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def negative_case(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        self.create_box('negative_case')
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            try:
                if result == 'PASS':
                    result = self.get_parsed_values(
                        xmlout, kwargs['notif_name'])

                    if str(kwargs['notif_name']) == result:
                        LOG.info('notif_name : %s' % result)
                        LOG.info('compare both notifications : PASS\n')
                        result = 'PASS'
                    else:
                        LOG.error('comparision failed : FAIL\n')
                        result = 'FAIL'
            except Exception as err:
                LOG.info(
                    'getting error from switch : PASS\n\n Error : %s' %
                    err)
                result = PASS

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'negative_case', d, result)

    def getconfig_port_label(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           port_label            : valid port label
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_port_label = kwargs['port_labels'].split(',')

        self.create_box('getconfig_port_label')
        xmlstr = self.create_xml_for_single_tag(
            'port-label', kwargs['port_labels'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-label')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-label')

                if str(gvn_port_ids) == str(result1) and str(gvn_port_label) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info('gvn_port_labels : %s\n\n' % gvn_port_label)
                    LOG.info('compare both port ids and port_labels : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_port_label', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_port_state(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           port_state            : valid port state
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_port_states = kwargs['port_states'].split(',')

        self.create_box('getconfig_port_state')
        xmlstr = self.create_xml_for_single_tag(
            'port-state', kwargs['port_states'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-state')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-state')

                if str(gvn_port_ids) == str(result1) and str(gvn_port_states) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
                    LOG.info('compare both port ids and port_states : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_port_state', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_port_status(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           port_label            : valid port label
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_port_status = kwargs['port_status'].split(',')

        self.create_box('getconfig_port_status')
        # xmlstr = self.create_xml_for_single_tag('port-status', kwargs['port_status'])
        # result = self.edit_config_opr()

        xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-status')
        xmlout, result = self.getconfig_rpc_request(
            xmlstr, kwargs['file_name'])
        if result == 'PASS':
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'port-status')

            if str(gvn_port_ids) == str(result1) and str(gvn_port_status) == str(result2):
                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_status : %s\n\n' % gvn_port_status)
                LOG.info('compare both port ids and port_status : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_port_status', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_lambda(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           port_lambda           : valid port lambda
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_lambdas = kwargs['lambdas'].split(',')

        self.create_box('getconfig_lambda')
        xmlstr = self.create_xml_for_single_tag('lambda', kwargs['lambdas'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'lambda')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'lambda')

                if str(gvn_port_ids) == str(result1) and str(gvn_lambdas) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                    LOG.info('compare both port ids and lambdas : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_lambdas', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_high_alarm(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           power_high_alarm      : valid power high alarm val
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_alarms = kwargs['power_high_alarms'].split(',')

        self.create_box('getconfig_power_high_alarms')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-alarm',
            kwargs['power_high_alarms'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-high-alarm')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-alarm')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_alarms) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_high_alarms : %s\n\n' %
                        gvn_power_high_alarms)
                    LOG.info(
                        'compare both port ids and power_high_alarms : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power_high_alarms', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_low_alarm(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           power_low_alarm       : valid power low alarm val
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_alarms = kwargs['power_low_alarms'].split(',')

        self.create_box('getconfig_power_low_alarm')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm',
            kwargs['power_low_alarms'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-low-alarm')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-alarm')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_alarms) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_low_alarms : %s\n\n' %
                        gvn_power_low_alarms)
                    LOG.info(
                        'compare both port ids and power_low_alarms : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power_low_alarms', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_high_warning_offset(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           port_label            : valid port label
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_warning_offsets = kwargs[
            'power_high_warning_offsets'].split(',')

        self.create_box('getconfig_power_high_warning_offset')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-warning-offset',
            kwargs['power_high_warning_offsets'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-high-warning-offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-warning-offset')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_warning_offsets) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_high_warning_offsets : %s\n\n' %
                        gvn_power_high_warning_offsets)
                    LOG.info(
                        'compare both port ids and power_high_warning_offsets : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'getconfig_power_high_warning_offsets',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_low_warning_offset(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	             : valid port ids
           power_low_warning_offsets : valid power low warning offsets val
           file_name                 : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_warning_offsets = kwargs[
            'power_low_warning_offsets'].split(',')

        self.create_box('getconfig_power_low_warning_offset')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset',
            kwargs['power_low_warning_offsets'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-low-warning-offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-warning-offset')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_warning_offsets) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_low_warning_offsets : %s\n\n' %
                        gvn_power_low_warning_offsets)
                    LOG.info(
                        'compare both port ids and power_low_warning_offsets : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'getconfig_power_low_warning_offsets',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_alarm_control(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           power_alarm_controls  : valid power_alarm_controls
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_controls = kwargs['power_alarm_controls'].split(',')

        self.create_box('getconfig_power_alarm_control')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-control',
            kwargs['power_alarm_controls'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-control')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-control')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_controls) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_power_alarm_controls)
                    LOG.info(
                        'gvn_power_alarm_controls : %s\n\n' %
                        gvn_power_alarm_controls)
                    LOG.info(
                        'compare both port ids and power_alarm_controls : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power_alarm_controls', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_alarm_status(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           power_alarm_status    : valid power alarm status
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_status = kwargs['power_alarm_status'].split(',')

        self.create_box('getconfig_power_alarm_status')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-status',
            kwargs['power_alarm_status'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-status')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-status')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_status) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_alarm_status : %s\n\n' %
                        gvn_power_alarm_status)
                    LOG.info(
                        'compare both port ids and power_alarm_status : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power_alarm_status', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power(self, **kwargs):
        """perform get operation for created power query
        Arguments:
           port_ids 	         : valid port ids
           powerval              : valid power val
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power = kwargs['power'].split(',')

        self.create_box('getconfig_power')
        xmlstr = self.create_xml_for_single_tag('power', kwargs['power'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'power')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power')

                if str(gvn_port_ids) == str(result1) and str(gvn_power) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info('gvn_power : %s\n\n' % gvn_power)
                    LOG.info('compare both port ids and power : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_offset(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	         : valid port ids
           offsets               : valid offsets
           file_name             : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_offsets = kwargs['offsets'].split(',')

        self.create_box('getconfig_offsets')
        xmlstr = self.create_xml_for_single_tag('offset', kwargs['offsets'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'offset')

                if str(gvn_port_ids) == str(result1) and str(gvn_offsets) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
                    LOG.info('compare both port ids and offsets : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_offsets', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_averaging_time_select(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	            : valid port ids
           averaging time select    : valid averaging time select
           file_name                : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_averaging_time_selects = kwargs[
            'averaging_time_selects'].split(',')

        self.create_box('getconfig_averaging_time_selects')
        xmlstr = self.create_xml_for_single_tag(
            'averaging-time-select',
            kwargs['averaging_time_selects'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'averaging-time-select')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'averaging-time-select')

                if str(gvn_port_ids) == str(result1) and str(gvn_averaging_time_selects) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_averaging_time_selects : %s\n\n' %
                        gvn_averaging_time_selects)
                    LOG.info(
                        'compare both port ids and averaging_time_selects : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_averaging_time_selects', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_alarm_hysteresis(self, **kwargs):
        """perform get operation for created power alarm hysteresis query
        Arguments:
           port_ids 	             : valid port ids
           power_alarm_hysteresis    : valid power_alarm_hysteresis
           file_name                 : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_hysteresis = kwargs[
            'power_alarm_hysteresis'].split(',')

        self.create_box('getconfig_power_alarm_hysteresis')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-hysteresis',
            kwargs['power_alarm_hysteresis'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-hysteresis')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-hysteresis')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_hysteresis) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_alarm_hysteresis : %s\n\n' %
                        gvn_power_alarm_hysteresis)
                    LOG.info(
                        'compare both port ids and power_alarm_hysteresis : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'getconfig_power_alarm_hysteresis', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_power_alarm_clear_holdoff(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
           port_ids 	                 : valid port ids
           power_alarm_clear_hold_off    : valid power_alarm_clear_hold_off val
           file_name                     : any file name
        """

        global sw_mgr
        global gvn_port_ids

        s = time.time()

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_clear_holdoff = kwargs[
            'power_alarm_clear_holdoff'].split(',')

        self.create_box('getconfig_power_alarm_clear_holdoff')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-clear-holdoff')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-clear-holdoff')

                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                    LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    LOG.info(
                        'gvn_power_alarm_clear_holdoff : %s\n\n' %
                        gvn_power_alarm_clear_holdoff)
                    LOG.info(
                        'compare both port ids and power_alarm_clear_holdoff : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'getconfig_power_alarm_clear_holdoff',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)
