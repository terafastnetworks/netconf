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
        groups = get_config_arg("login_credentials", "groups").split(',')
        passwords = get_config_arg("login_credentials", "passwords").split(',')
        users = get_config_arg("login_credentials", "users").split(',')
        try:
            if groups[0] == 'user':
              username = users[0]
              password = passwords[0]
            elif groups[1] == 'user':
              username = users[1]
              password = passwords[1]
            else:
              LOG.error("Please give 'user' and 'view'")
        except:
            LOG.error("Please give correct group names other than admin")

        timeout = get_config_arg("login_credentials", "timeout")

        LOG.info("Connecting switch <IP:Port = %s:%s> using <%s:%s>\n" % (host, port, username, password))
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
        f = open('admin/outputXml/%s' % file_name, 'w')
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
        tagVal = 'None'
        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        enable_notifications = collection.getElementsByTagName(
            "enable-notifications")[0]
        # print "enable_notifications : ", enable_notifications
        try:
            tagVal = str(enable_notifications.childNodes[0].data)
        except Exception as err:
            LOG.error('There is no object coming under enable_notifications container\n')
        # print "tagVal :", tagVal

        LOG.info('-----[ validate notification information ]-----\n\n')

        LOG.info('parsed notifications : %s' % tagVal)

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
            LOG.info("-----[ pass xml for edit-config operation ]-----\n\n%s\n" % self.prettify(xmlstr))

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

    def editconfig_notif_activity(self, **kwargs):
        """create notif_port notification using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare both
        notifications
        """

        s = time.time()
        #self.create_box('test_editconfig_notif_port')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 
            if str(kwargs['notif_name']) == result:
                #LOG.info('notif_name : %s' % result)
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
        #self.create_box('test_editconfig_notif_port_power')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

            if kwargs['notif_name'] == result:
                #LOG.info('notif_name : %s' % result)
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
        #self.create_box('test_editconfig_notif_port_power_warn')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            #LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

            if kwargs['notif_name'] == result:
                #LOG.info('notif_name : %s' % result)
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
        #self.create_box('test_editconfig_notif_switch')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            #LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

            if kwargs['notif_name'] == result:
                #LOG.info('notif_name : %s' % result)
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
        #self.create_box('test_editconfig_notif_system')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            #LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

            if kwargs['notif_name'] == result:
                #LOG.info('notif_name : %s' % result)
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
        #self.create_box('test_editconfig_with_all_notif')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            #LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            enable_notifications = Element(
                'plts:enable-notifications',
                {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

            xmlstr = tostring(enable_notifications)
            LOG.info('-----[ create xml for get-config operation ]-----\n\n%s\n' % self.prettify(xmlstr))
            # print "xmlstr is : %s\n\n" % xmlstr
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result = self.get_parsed_values(xmlout, kwargs['notif_name'])
            LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

            if kwargs['notif_name'] == result:
                #LOG.info('notif_name : %s' % result)
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


        enable_notifications = Element(
            'plts:enable-notifications',
            {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

        xmlstr = tostring(enable_notifications)
        LOG.info('-----[ create xml for get/getconfig operation ]-----\n\n%s\n' % self.prettify(xmlstr))
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

    def get_notif_activity(self, **kwargs):
        """perform get operation for created port-label query
        Arguments:
        """

        global sw_mgr

        s = time.time()

        #self.create_box('get_notif_port_enable_notification')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                LOG.info('given notif_names : %s' %  kwargs['notif_name']) 
                if str(kwargs['notif_name']) == result:
                    #LOG.info('notif_name : %s' % result)
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

        #self.create_box('get_notif_port_power_enable_notification')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])

                LOG.info('given notif_names : %s' %  kwargs['notif_name']) 
                if str(kwargs['notif_name']) == result:
                    #LOG.info('notif_name : %s' % result)
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

        #self.create_box('get_notif_port_power_warn_enable_notification')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])
                LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

                if str(kwargs['notif_name']) == result:
                    #LOG.info('notif_name : %s' % result)
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

        #self.create_box('get_notif_switch')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])
                LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

                if str(kwargs['notif_name']) == result:
                    #LOG.info('notif_name : %s' % result)
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

        #self.create_box('get_notif_system_enable_notification')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result = self.get_parsed_values(xmlout, kwargs['notif_name'])
                LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

                if str(kwargs['notif_name']) == result:
                    #LOG.info('notif_name : %s' % result)
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

        #self.create_box('negative_case')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml(kwargs['notif_name'])
        result = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr()
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            try:
                if result == 'PASS':
                    result = self.get_parsed_values(
                        xmlout, kwargs['notif_name'])
                    LOG.info('given notif_names : %s' %  kwargs['notif_name']) 

                    if str(kwargs['notif_name']) == result:
                        #LOG.info('notif_name : %s' % result)
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
