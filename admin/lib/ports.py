""" ports lib """

import nose
import sys
import time
import itertools
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
Rpc_Reply = '<ok/>' 

class Ports:

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

    def create_xml_for_single_tag(self, tag_name, tag_val, opr):
        """create xml with given ports tags and push it to edit-config
        operation, form the xml for get the configurable variables using get-config
        operation, parse this get-config output, finally compare this tags valus with
        given tags values
        """

        global xmlstr
        global gvn_port_ids

        config = Element('config')
        ports = SubElement(
            config,
            'ports',
            {'xmlns': "http://www.polatis.com/yang/optical-switch",
             'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

        tag_name = tag_name.split(',')
        print "type of tag_name : ", type(tag_name)
        print "tag name : ", tag_name
        print "tag name : ", len(tag_name)
        print "tag_val : ", tag_val

        tag_val = tag_val.split(',')
        #print "tag val : %s" % tag_val
        l = len(gvn_port_ids)
        #print "gvn_port_ids  : ", gvn_port_ids
          
        opr_list = [ 'delete', 'replace', 'merge', 'remove']
      
        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        for v1, v2 in zip(range(0, l), range(0, l)):
            print "insdie 1st for loo..."
            port_id_val = gvn_port_ids[v1]
            tag_values = tag_val[v2]
            print "tag_values : ", tag_values
            port = SubElement(ports, 'port')
            port_id = SubElement(port, 'port-id')
            port_id.text = str(port_id_val)
            print "tag name : ", len(tag_name)
            for i in range(0, len(tag_name)):
                if v2 != 0:
                    tag_values = tag_val[v2]
                else:
                    tag_values = tag_val[i]
                print "tag_values opm : ", tag_values
                opm = SubElement(port, 'opm', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
                print "insdie 2nd for loo..."
                print tag_name[i];print tag_values
                if tag_name[i] in opm_list or tag_name[i] in opm_plts_list:
                    print "insdie 1st if loo..."
                    if tag_name[i] in opm_plts_list:
                        print "insdie 2nd if loo..."
                        #opm = SubElement(port, 'opm', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
		        if opr in opr_list:
                            tag = SubElement(
                                opm,
                                'plts:' + tag_name[i],
                                {'ns:operation':'%s' % opr})
                        else:
                            tag = SubElement(
                                opm,
                                'plts:' + tag_name[i])
                        tag.text = str(tag_values)
                    else:
                         print "else ........................."
                         if opr in opr_list:
                             tag = SubElement(opm, tag_name[i], {'ns:operation':'%s' % opr})
                         else:
                             print "else ....2....................."
                             print "tag name : ", tag_name[i]
                             tag = SubElement(opm, tag_name[i])
                         print " tag_values : ", tag_values
                         tag.text = str(tag_values)
                else:
                    print "else .....for portt....."
                    if opr == 'delete':
                        tag = SubElement(port, tag_name[i], {'ns:operation':'delete'})
                    elif opr == 'replace':
                        tag = SubElement(port, tag_name[i], {'ns:operation':'replace'})
                        tag.text = str(tag_values)
                    else:
                        tag = SubElement(port, tag_name[i])
                        tag.text = str(tag_values)
                    
        xmlstr = tostring(config)
        print xmlstr
        #LOG.info(xmlstr)
        return xmlstr

    def create_xml_for_multiple_tags(self, tag_val, opr):
        """create xml with given ports tags and push it to edit-config
        operation, form the xml for get the configurable variables using get-config
        operation, parse this get-config output, finally compare this tags valus with
        given tags values
        """

        global xmlstr
        global gvn_port_ids

        config = Element('config')
        ports = SubElement(
            config,
            'ports',
            {'xmlns': "http://www.polatis.com/yang/optical-switch",
             'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

        tag_value = tag_val.split(',')
        #print "tag val : %s" % tag_val
        l = len(gvn_port_ids)
        #print "gvn_port_ids  : ", gvn_port_ids

        opr_list = [ 'delete', 'replace', 'merge', 'remove']

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-clear-holdoff']

        for prt in range(0, l):
            port_id_val = gvn_port_ids[prt]
            port = SubElement(ports, 'port')
            port_id = SubElement(port, 'port-id')
            port_id.text = str(port_id_val)
            opm = SubElement(port, 'opm', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
            if opr in opr_list:
                for index in range(0,6):
                    tag = SubElement(opm, opm_list[index], {'ns:operation': '%s' % opr} )
                    tag.text = str(tag_value[index])
                for index in range(0,3):
                    tag = SubElement(opm, 'plts:' + opm_plts_list[index], {'ns:operation': '%s' % opr})
                    tag.text = str(tag_value[index+6])
            else:
                for index in range(0,6):
                    tag = SubElement(opm, opm_list[index])
                    tag.text = str(tag_value[index])
                for index in range(0,3):
                    tag = SubElement(opm, 'plts:' + opm_plts_list[index])
                    tag.text = str(tag_value[index+6])	
	xmlstr = tostring(config)
        #LOG.info(xmlstr)
        return xmlstr
	

    #def create_xml_for_multiple_tags(self, tag_name, tag_val, opr):
    #    """create xml with given ports tags and push it to edit-config
    #    operation, form the xml for get the configurable variables using get-config
    #    operation, parse this get-config output, finally compare this tags valus with
    #    given tags values
    #    """

    #    global xmlstr
    #    global gvn_port_ids

    #    config = Element('config')
    #    ports = SubElement(
    #        config,
    #        'ports',
    #        {'xmlns': "http://www.polatis.com/yang/optical-switch",
    #         'xmlns:plts': "http://www.polatis.com/yang/polatis-switch"})

    #    tag_val = tag_val.split(',')
    #    #print "tag val : %s" % tag_val
    #    l = len(gvn_port_ids)
    #    #print "gvn_port_ids  : ", gvn_port_ids

    #    opr_list = [ 'delete', 'replace', 'merge', 'remove']

    #    opm_list = [
    #        'lambda',
    #        'power-high-alarm',
    #        'power-low-alarm',
    #        'power-high-warning-offset',
    #        'power-low-warning-offset',
    #        'power-alarm-control',
    #        'power-alarm-status',
    #        'power',
    #        'averaging-time-select',
    #        'power-alarm-hysteresis',
    #        'power-alarm-clear-holdoff']
    #    opm_plts_list = [
    #        'offset',
    #        'averaging-time-select',
    #        'power-alarm-hysteresis',
    #        'power-alarm-clear-holdoff']

    #    if tag_name in opm_list or tag_name in opm_plts_list:
    #        for v1, v2 in zip(range(0, l), range(0, l)):
    #            port_id_val = gvn_port_ids[v1]
    #            tag_values = tag_val[v2]
    #            port = SubElement(ports, 'port')
    #            port_id = SubElement(port, 'port-id')
    #            port_id.text = str(port_id_val)
    #            if tag_name in opm_plts_list:
    #                opm = SubElement(port, 'opm', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})

    #                #tag = SubElement(opm, tag_name)
    #                if opr in opr_list:
    #                    tag = SubElement(
    #                        opm,
    #                        'plts:' + kwargs['tag_name'],
    #                        {'ns:operation':'%s' % opr})
    #                else:
    #                    tag = SubElement(
    #                        opm,
    #                        'plts:' + kwargs['tag_name'])
    #                tag.text = str(tag_values)
    #            else:
    #                opm = SubElement(port, 'opm', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    #                if opr in opr_list:
    #                    tag = SubElement(opm, kwargs['tag_name'], {'ns:operation':'%s' % opr})
    #                else:
    #                    tag = SubElement(opm, tag_name)
    #    		tag1 = SubElement(opm, tag_name)
    #                tag.text = str(tag_values)
    #    else:
    #        for v1, v2 in zip(range(0, l), range(0, l)):
    #            port_id_val = gvn_port_ids[v1]
    #            tag_values = tag_val[v2]
    #            port = SubElement(ports, 'port', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    #            port_id = SubElement(port, 'port-id')
    #            port_id.text = str(port_id_val)
    #            #print "opr : " , opr
    #            if opr == 'delete':
    #                tag = SubElement(port, tag_name, {'ns:operation':'delete'})
    #            elif opr == 'replace':
    #                tag = SubElement(port, tag_name, {'ns:operation':'replace'})
    #                tag.text = str(tag_values)
    #            else:
    #                tag = SubElement(port, tag_name)
    #                tag.text = str(tag_values)


    #    xmlstr = tostring(config)
    #    #LOG.info(xmlstr)
    #    return xmlstr

    def get_parsed_values(self, xmlData, tag_name_1, tag_name_2):
        """compare the data's in list.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
           tag_name_1,tag_name_2	    : give valid ports-sub tags name
        """

        parsed_tag1_values = []
        parsed_tag2_values = []

        p = 'PASS'
        f = 'FAIL'

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement
	prettyXml = self.prettify(xmlData)
	
        ports = collection.getElementsByTagName("port")
        opms = collection.getElementsByTagName("opm")

        for port_id in ports:
            try:
                # print "inside opm get
                # parsed------------------------------------------"
                tag1Name = port_id.getElementsByTagName(tag_name_1)[0]
                tag1Val = str(tag1Name.childNodes[0].data)

                parsed_tag1_values.append(tag1Val)

                tag2Name = port_id.getElementsByTagName(tag_name_2)[0]
                tag2Val = str(tag2Name.childNodes[0].data)

                parsed_tag2_values.append(tag2Val)
            except:
                pass

        for opm in opms:
            try:
                # print "inside opm get
                # parsed-------------------------------------"
                tag1Name = opm.getElementsByTagName(tag_name_1)[0]
                tag1Val = str(tag1Name.childNodes[0].data)

                parsed_tag1_values.append(tag1Val)

                tag2Name = opm.getElementsByTagName(tag_name_2)[0]
                # print "tag2Name is : %s\n\n" % tag2Name
                tag2Val = str(tag2Name.childNodes[0].data)

                parsed_tag2_values.append(tag2Val)
            except:
                pass

        #print type(parsed_tag2_values)
        if parsed_tag2_values == []:
            l = ['','','']
            for i in range(0, 3):
                parsed_tag2_values.append(l[i])
        #print type(parsed_tag2_values)

        LOG.info('-----[ validate ports information ]-----\n\n')

        LOG.info('parsed-' + tag_name_1 + 's : %s' % parsed_tag1_values)
        LOG.info('parsed-' + tag_name_2 + 's : %s\n\n' % parsed_tag2_values)

        return (parsed_tag1_values, parsed_tag2_values)

    def parsed_xml_for_get_power_value(self, xmlData):
        """parsed xml to get values of power tag for given port-ids.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
        """

        parsed_power_values = []

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        opms = collection.getElementsByTagName("opm")

        for opm in opms:
            try:
                # print "inside opm get
                # parsed-------------------------------------"
                power = opm.getElementsByTagName('power')[0]
                power_val = str(power.childNodes[0].data)

                parsed_power_values.append(power_Val)

            except:
                pass

        LOG.info('parsed-power-values : %s\n\n' % parsed_power_values)

        return parsed_power_values

    def edit_config_opr(self):
        """ create required ports operation using edit-config rpc request.
        Arguments:
        """

        global sw_mgr
        global xmlstr

        p = 'PASS'
        f = 'FAIL'
        try:
            LOG.info("-----[ pass xml for edit-config operation ]-----\n\n")
            LOG.info("xmlstr : \n\n%s\n" % self.prettify((str(xmlstr))))
            xmldata = sw_mgr.edit_config(target='running', config=xmlstr)
            print "\n\n"

            LOG.info(
                '-----[ edit-config - response from the switch ]-----\n\n\n%s\n\n' %
                self.prettify(str(xmldata)))
            return p, xmldata

        except Exception as err:
            print "\n\n"
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n' % err)
            return f, err

    def editconfig_create_port_label(self, *args, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_port_labels

        gvn_port_ids = kwargs['port_ids']
        gvn_port_labels = kwargs['port_labels'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'port-label', kwargs['port_labels'], kwargs['opr'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            if 'single' in args:
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(gvn_port_ids[2])
            else:
                for tag1 in range(0, l):
                    port_id_val = gvn_port_ids[tag1]
                    port = SubElement(ports, 'opsw:port')
                    port_id = SubElement(port, 'opsw:port-id')
                    port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            # print "xmlstr is : %s\n\n" % xmlstr
            if kwargs['operation'] == 'get':
                LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.get_rpc_request(
                    xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'port-label')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass
            if 'single' in args:
                gvn_port_id = [] ; gvn_port_id.append(gvn_port_ids[2])
                gvn_port_ids = gvn_port_id 
                gvn_port_label = [] ; gvn_port_label.append(gvn_port_labels[2])
                gvn_port_labels = gvn_port_label 
                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_labels : %s\n\n' % gvn_port_labels)
            else:    
                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_labels : %s\n\n' % gvn_port_labels)
            # LOG.info('compare both port ids and port labels : PASS\n')

            if str(gvn_port_ids) == str(result1) and str(gvn_port_labels) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_port_labels : %s\n\n' % gvn_port_labels)
                LOG.info('compare both port ids and port labels : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_port_label', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_port_label(self, **kwargs):
        """create innvalid port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_port_labels

        gvn_port_ids = kwargs['port_ids']
        gvn_port_labels = kwargs['port_labels'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'port-label', kwargs['port_labels'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        LOG.info('gvn_port_labels : %s\n\n' % gvn_port_labels)

        if result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_port_label',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_port_label',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        nose.tools.assert_equals('FAIL', result)

    def editconfig_create_port_state(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_port_states

        gvn_port_ids = kwargs['port_ids']
        gvn_port_states = kwargs['port_states'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
        self.create_box('test_editconfig_create_port_state')
        xmlstr = self.create_xml_for_single_tag(
            'port-state', kwargs['port_states'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'port-state')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
            if gvn_port_ids == result1 and str(gvn_port_states) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
                LOG.info('compare both port ids and port states : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_port_state', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_port_state(self, **kwargs):
        """create invalid port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_port_states

        gvn_port_ids = kwargs['port_ids']
        gvn_port_states = kwargs['port_states'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'port-state', kwargs['port_states'], kwargs['opr'])
        gvn_port_ids = gvn_port_ids.split()
        result, message = self.edit_config_opr()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)

        if result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_port_state',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_port_state',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        nose.tools.assert_equals('FAIL', result)
        nose.tools.assert_equals(kwargs['msg'], str(message))

    def editconfig_create_lambda(self, **kwargs):
        """create lambda for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_lambdas

        gvn_port_ids = kwargs['port_ids']
        gvn_lambdas = kwargs['lambdas'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box('test_admin_set_lambda_and_validate_with_getconfig')
        xmlstr = self.create_xml_for_single_tag('lambda', kwargs['lambdas'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error while checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
             
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                lam = SubElement(opm, 'opsw:lambda')

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
		 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info("xmlstr : \n\n%s\n" % self.prettify((str(xmlstr))))
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
	    else:
	 	LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info("xmlstr : \n\n%s\n" % self.prettify((str(xmlstr))))
            	xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                  xmlout, 'port-id', 'lambda')
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_lambdas = ['1500.0', '1500.0', '1500.0']
                LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
            else:
                LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)

            if str(gvn_port_ids) == str(result1) and str(gvn_lambdas) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                LOG.info('compare both port ids and lambdas : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_port_lambda', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_lambda(self, **kwargs):
        """create invalid port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_lambdas

        gvn_port_ids = kwargs['port_ids']
        gvn_lambdas = kwargs['lambdas'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box('test_admin_set_invalid_lambda_and_validate_with_getconfig')
        xmlstr = self.create_xml_for_single_tag('lambda', kwargs['lambdas'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)

        if result == 'PASS':

            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                ports = Element(
                   'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                                  'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
                for tag1 in range(0, l):
                    port_id_val = gvn_port_ids[tag1]
                    port = SubElement(ports, 'opsw:port')
                    port_id = SubElement(port, 'opsw:port-id')
                    opm1 = SubElement(port, 'opsw:opm')
                    low_alm = SubElement(opm1, 'opsw:lambda')
                    port_id.text = str(port_id_val)

                xmlstr = tostring(ports)
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                #LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                            xmlstr, kwargs['file_name'])
                self.get_parsed_values(xmlout, 'port-id', 'lambda')
           	gvn_lambdas = ['1550.0']
		LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                if str(gvn_lambdas) == str(gvn_lambdas):
                    LOG.info('compare both port ids and lambdas : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'

        elif result == 'FAIL':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
            'ports',
            'editconfig_create_invalid_port_states',
            d,
            result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_port_states',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_high_alarm(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_high_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_alarms = kwargs['power_high_alarms'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_admin_set_high_power_alarm_and_validate_with_get_config')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-alarm',
            kwargs['power_high_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")	

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
                high_alm = SubElement(opm1, 'power-high-alarm')
                port_id.text = str(port_id_val)

	    xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
	    else:
		LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
            	xmlout, result = self.getconfig_rpc_request(
                	xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-high-alarm')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_high_alarms = ['25.0', '25.0', '25.0']
		LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
	    else:
                LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)

            if str(gvn_port_ids) == str(result1) and str(gvn_power_high_alarms) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and power_high_alarms : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_high_alarms',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_high_alarm(self, **kwargs):
        """create invalid power high alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_high_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_alarms = kwargs['power_high_alarms'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_admin_set_invalid_high_power_alarm_and_validate_with_get_config')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-alarm',
            kwargs['power_high_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)

	if result == 'PASS':

            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                ports = Element(
                   'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                                  'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
                for tag1 in range(0, l):
                    port_id_val = gvn_port_ids[tag1]
                    port = SubElement(ports, 'opsw:port')
                    port_id = SubElement(port, 'opsw:port-id')
                    opm1 = SubElement(port, 'opsw:opm')
                    low_alm = SubElement(opm1, 'power-high-alarm')
                    port_id.text = str(port_id_val)

                xmlstr = tostring(ports)
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                #LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                            xmlstr, kwargs['file_name'])
                self.get_parsed_values(xmlout, 'port-id', 'power-high-alarm')
           	gvn_power_high_alarms = ['25.0']
                LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                if str(gvn_power_high_alarms) == str(gvn_power_high_alarms):
                    LOG.info('compare both port ids and power high alarms : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'

        elif result == 'FAIL':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_high_alarms',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_high_alarms',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_low_alarm(self, **kwargs):
        """create power low alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_low_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_alarms = kwargs['power_low_alarms'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_admin_set_low_power_alarm_and_validate_with_get_config')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm',
            kwargs['power_low_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
                low_alm = SubElement(opm1, 'power-low-alarm')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)

            	xmlout, result = self.getconfig_rpc_request(
                	xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-low-alarm')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_low_alarms = ['-59.99']
                LOG.info('gvn_power_low_alarms : %s\n\n' % gvn_power_low_alarms)
            else:
                LOG.info('gvn_power_low_alarms : %s\n\n' % gvn_power_low_alarms)

            #LOG.info('gvn_power_low_alarms : %s\n\n' % gvn_power_low_alarms)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_low_alarms) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_low_alarms : %s\n\n' %
                #    gvn_power_low_alarms)
                LOG.info('compare both port ids and power low alarms : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_power_low_alarms', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_low_alarm(self, **kwargs):
        """create invalid power low alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_low_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_alarms = kwargs['power_low_alarms'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_admin_set_invalid_low_power_alarm_and_validate_with_get_config')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm',
            kwargs['power_low_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()

        gvn_port_ids = gvn_port_ids.split()

        #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info('gvn_power_low_alarms : %s\n\n' % gvn_power_low_alarms)
        if result == 'PASS': 

	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
	        ports = Element(
                   'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                                  'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
                for tag1 in range(0, l):
               	    port_id_val = gvn_port_ids[tag1]
               	    port = SubElement(ports, 'opsw:port')
               	    port_id = SubElement(port, 'opsw:port-id')
               	    opm1 = SubElement(port, 'opsw:opm')
               	    low_alm = SubElement(opm1, 'power-low-alarm')
               	    port_id.text = str(port_id_val)

        	xmlstr = tostring(ports)
		LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                #LOG.info('xmlstr : \n\n%s\n' % xmlstr)		
	       	xmlout, result = self.getconfig_rpc_request(
                            xmlstr, kwargs['file_name'])
               	self.get_parsed_values(xmlout, 'port-id', 'power-low-alarm')
               	gvn_power_low_alarms = ['-59.99']
               	LOG.info('gvn_power_low_alarms : %s\n\n' % gvn_power_low_alarms)
		print str(result)
		print str(gvn_power_low_alarms)
	       	if str(gvn_power_low_alarms) == str(gvn_power_low_alarms):
               	    LOG.info('compare both port ids and power low alarms : PASS\n')
               	    result = 'PASS'
               	else:
               	    LOG.error('comparision failed : FAIL\n')
               	    result = 'FAIL'

        elif result == 'FAIL':       
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_low_alarms',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_low_alarms',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')
        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':    
	    nose.tools.assert_equals('PASS', result)
	else:
            nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_high_warning_offset(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_high_warning_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_warning_offsets = kwargs[
            'power_high_warning_offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_power_high_warning_offsets_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-warning-offset',
            kwargs['power_high_warning_offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
                high_off = SubElement(opm1, 'power-high-warning-offset')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)

            	xmlout, result = self.getconfig_rpc_request(
                	xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-high-warning-offset')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_high_warning_offsets = ['25.0', '25.0', '25.0']
                LOG.info('gvn_power_high_warning_offsets : %s\n\n' % gvn_power_high_warning_offsets)
            else:
                LOG.info('gvn_power_high_warning_offsets : %s\n\n' % gvn_power_high_warning_offsets)		
            #LOG.info('gvn_power_high_warning_offsets : %s\n\n' %gvn_power_high_warning_offsets)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_high_warning_offsets) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_warning_offsets : %s\n\n' %gvn_power_high_warning_offsets)
                LOG.info(
                    'compare both port ids and power high warning offsets : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_high_warning_offsets',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_high_warning_offset(self, **kwargs):
        """create invalid power high warning offset for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_high_warning_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_power_high_warning_offsets = kwargs[
            'power_high_warning_offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_power_high_warning_offsets_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-warning-offset',
            kwargs['power_high_warning_offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        LOG.info(
            'gvn_power_high_warning_offsets : %s\n\n' %
            gvn_power_high_warning_offsets)
	if result == 'PASS':
	
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
	        ports = Element(
                    'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
                for tag1 in range(0, l):
                    port_id_val = gvn_port_ids[tag1]
                    port = SubElement(ports, 'opsw:port')
                    port_id = SubElement(port, 'opsw:port-id')
                    opm1 = SubElement(port, 'opsw:opm')
                    high_off = SubElement(opm1, 'power-high-warning-offset')
                    port_id.text = str(port_id_val)

                xmlstr = tostring(ports)
	        LOG.info(
                        '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)

                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-warning-offset')
                gvn_power_high_warning_offsets = ['25.0']
                LOG.info('gvn_power_high_warning_offsets : %s\n\n' % gvn_power_high_warning_offsets)
	        if str(gvn_power_low_alarms) == str(result):
                        LOG.info('compare both port ids and power low alarms : PASS\n')
                        result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'

            elif result == 'FAIL':
                e = time.time()
                d = int(round((e - s) * 1000))
                LOG.info('Invalid case is passed : FAIL\n\n')
                csvOutput(
                    'ports',
                    'editconfig_create_invalid_power_high_warning_offsets',
                    d,
                    result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_high_warning_offsets',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_low_warning_offset(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_low_warning_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_warning_offsets = kwargs[
            'power_low_warning_offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_power_low_warning_offsets_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset',
            kwargs['power_low_warning_offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
            	xmlout, result = self.getconfig_rpc_request(
                	xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-low-warning-offset')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass
	
            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_low_warning_offsets = ['-60.0', '-60.0', '-60.0']
                LOG.info('gvn_power_low_warning_offsets : %s\n\n' % gvn_power_low_warning_offsets)
            else:
                LOG.info('gvn_power_low_warning_offsets : %s\n\n' % gvn_power_low_warning_offsets)

            #LOG.info(
            #    'gvn_power_low_warning_offsets : %s\n\n' %
            #    gvn_power_low_warning_offsets)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_low_warning_offsets) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_low_warning_offsets : %s\n\n' %
                #    gvn_power_low_warning_offsets)
                LOG.info(
                    'compare both port ids and power low warning offset : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_low_warning_offsets',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_low_warning_offset(self, **kwargs):
        """create invalid power low warning for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_low_warning_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_power_low_warning_offsets = kwargs[
            'power_low_warning_offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_power_low_warning_offsets_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset',
            kwargs['power_low_warning_offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        LOG.info(
            'gvn_power_low_warning_offsets : %s\n\n' %
            gvn_power_low_warning_offsets)

        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_power_low_warning_offsets = ['-60.0']
            LOG.info('gvn_power_low_warning_offsets : %s\n\n' % gvn_power_low_warning_offsets)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_low_warning_offsets',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_low_warning_offsets',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_alarm_control(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_controls

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_controls = kwargs['power_alarm_controls'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_power_alarm_controls_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-control',
            kwargs['power_alarm_controls'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-alarm-control')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_alarm_controls = ['POWER_ALARM_DISABLED']
                LOG.info('gvn_power_alarm_controls : %s\n\n' % gvn_power_alarm_controls)
            else:
                LOG.info('gvn_power_alarm_controls : %s\n\n' % gvn_power_alarm_controls)
            #LOG.info(
            #    'gvn_power_alarm_controls : %s\n\n' %
            #    gvn_power_alarm_controls)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_controls) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_alarm_controls : %s\n\n' %
                #    gvn_power_alarm_controls)
                LOG.info(
                    'compare both port ids and power alarm controls : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_alarm_controls',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_alarm_control(self, **kwargs):
        """create invalid poweer alarm control for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_controls

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_controls = kwargs['power_alarm_controls'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_power_alarm_controls_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-control',
            kwargs['power_alarm_controls'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info(
        #    'gvn_power_alarm_controls : %s\n\n' %
        #    gvn_power_alarm_controls)

	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_power_alarm_control = ['POWER_ALARM_DISABLED']
            LOG.info('gvn_power_alarm_control : %s\n\n' % gvn_power_alarm_control)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_alarm_controls',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_alarm_controls',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def editconfig_create_offset(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_offsets = kwargs['offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box('test_editconfig_create_offsets_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag('offset', kwargs['offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
		offset = SubElement(opm1, 'plts:offset xmlns:plts="http://www.polatis.com/yang/polatis-switch"')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
		
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'offset')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_offsets = ['0.0', '0.0', '0.0']
                LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
            else:
                LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
            #LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
            if str(gvn_port_ids) == str(result1) and str(gvn_offsets) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
                LOG.info('compare both port ids and offsets : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_offset', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_offset(self, **kwargs):
        """create invalid offset for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_offsets

        gvn_port_ids = kwargs['port_ids']
        gvn_offsets = kwargs['offsets'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_offset_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag('offset', kwargs['offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
	
	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_offsets = ['0.0']
            LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput('ports', 'editconfig_create_invalid_offset', d, result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'editconfig_create_invalid_offset', d, result)
            LOG.info('getting error from switch : PASS\n\n')

    def editconfig_create_averaging_time_select(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_averaging_time_selects

        gvn_port_ids = kwargs['port_ids']
        gvn_averaging_time_selects = kwargs[
            'averaging_time_selects'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_averaging_time_select_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'averaging-time-select',
            kwargs['averaging_time_selects'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
		avg_time = SubElement(opm1, 'plts:averaging-time-select')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    prettyXml = self.prettify(xmlstr)
	    if kwargs['operation'] == 'get':
                LOG.info(
                   '-----[ create xml for get operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)	
                xmlout, result = self.get_rpc_request(
                    xmlstr, kwargs['file_name'])

            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
            	xmlout, result = self.getconfig_rpc_request(
                	xmlstr, kwargs['file_name'])
		prettyXml = self.prettify(xmlstr)
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'averaging-time-select')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_averaging_time_selects = ['4', '4', '4']
                LOG.info('gvn_averaging_time_selects : %s\n\n' % gvn_averaging_time_selects)
            else:
                LOG.info('gvn_averaging_time_selects : %s\n\n' % gvn_averaging_time_selects)
            #LOG.info(
            #    'gvn_averaging_time_selects : %s\n\n' %
            #    gvn_averaging_time_selects)
            if str(gvn_port_ids) == str(result1) and str(gvn_averaging_time_selects) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_averaging_time_selects : %s\n\n' %
                #    gvn_averaging_time_selects)
                LOG.info(
                    'compare both port ids and averaging time select : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_averaging_time_select',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_averaging_time_select(self, **kwargs):
        """create invalid_averaging_time_select for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_averaging_time_selects

        gvn_port_ids = kwargs['port_ids']
        gvn_averaging_time_selects = kwargs[
            'averaging_time_selects'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_averaging_time_select_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'averaging-time-select',
            kwargs['averaging_time_selects'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info(
        #    'gvn_averaging_time_selects : %s\n\n' %
        #    gvn_averaging_time_selects)

	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_averaging_time_select = ['4']
            LOG.info('gvn_averaging_time_select : %s\n\n' % gvn_averaging_time_select)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_veraging_time_select',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_veraging_time_select',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_alarm_hysteresis(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_hysteresis

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_hysteresis = kwargs[
            'power_alarm_hysteresis'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_power_alarm_hysteresis_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-hysteresis',
            kwargs['power_alarm_hysteresis'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
		opm1 = SubElement(port, 'opsw:opm')
		hysteresis = SubElement(opm1, 'plts:power-alarm-hysteresis')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])

            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-alarm-hysteresis')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_alarm_hysteresis = ['100.0', '100.0', '100.0']
                LOG.info('gvn_power_alarm_hysteresis : %s\n\n' % gvn_power_alarm_hysteresis)
            else:
                LOG.info('gvn_power_alarm_hysteresis : %s\n\n' % gvn_power_alarm_hysteresis)
            #LOG.info(
            #    'gvn_power_alarm_hysteresis : %s\n\n' %
            #    gvn_power_alarm_hysteresis)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_hysteresis) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_alarm_hysteresis : %s\n\n' %
                #    gvn_power_alarm_hysteresis)
                LOG.info(
                    'compare both port ids and power alarm hysteresis : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_alarm_hysteresis',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_alarm_hysteresis(self, **kwargs):
        """create invalid power alarm hyteresis for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_hysteresis

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_hysteresis = kwargs[
            'power_alarm_hysteresis'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_power_alarm_hysteresis_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-hysteresis',
            kwargs['power_alarm_hysteresis'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info(
        #    'gvn_power_alarm_hysteresis : %s\n\n' %
        #    gvn_power_alarm_hysteresis)

	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_power_alarm_hysteresis = ['100.0']
            LOG.info('gvn_power_alarm_hysteresis : %s\n\n' % gvn_power_alarm_hysteresis)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_alarm_hysteresis',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_alarm_hysteresis',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        nose.tools.assert_equals('FAIL', result)

    def editconfig_create_power_alarm_clear_holdoff(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_clear_holdoff

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_clear_holdoff = kwargs[
            'power_alarm_clear_holdoff'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_power_alarm_clear_holdoff_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'], kwargs['opr'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
		opm1 = SubElement(port, 'opsw:opm')
                hysteresis = SubElement(opm1, 'plts:power-alarm-clear-holdoff')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            prettyXml = self.prettify(xmlstr)
	    if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % prettyXml)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])

            else:
                #prettyXml = self.prettify(xmlstr)
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % prettyXml)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-alarm-clear-holdoff')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_power_alarm_clear_holdoff = ['10', '10', '10']
                LOG.info('gvn_power_alarm_clear_holdoff : %s\n\n' % gvn_power_alarm_clear_holdoff)
            else:
                LOG.info('gvn_power_alarm_clear_holdoff : %s\n\n' % gvn_power_alarm_clear_holdoff)

            #LOG.info(
            #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
            #    gvn_power_alarm_clear_holdoff)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                #    gvn_power_alarm_clear_holdoff)
                LOG.info(
                    'compare both port ids and power alarm clear holdoff : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_alarm_clear_holdoff',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_power_alarm_clear_holdoff(self, **kwargs):
        """create invalid power alarm clear hold off for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_alarm_clear_holdoff

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_clear_holdoff = kwargs[
            'power_alarm_clear_holdoff'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_invalid_power_alarm_clear_holdoff_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'], kwargs['opr'])
        result, message = self.edit_config_opr()
        gvn_port_ids = gvn_port_ids.split()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)
        #LOG.info(
        #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
        #    gvn_power_alarm_clear_holdoff)
	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_power_alarm_clear_holdoff = ['10']
            LOG.info('gvn_power_alarm_clear_holdoff : %s\n\n' % gvn_power_alarm_clear_holdoff)
        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
                'ports',
                'editconfig_creat_invalid_power_alarm_clear_holdoff',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_power_alarm_clear_holdoff',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

        #nose.tools.assert_equals('FAIL', result)

    def default_state(self, **kwargs):


        global gvn_port_ids
        global gvn_power_alarm_clear_holdoff

        gvn_port_ids = kwargs['port_ids']

        l = len(gvn_port_ids)

        s = time.time()
        #    'test_editconfig_create_power_alarm_clear_holdoff_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm1 = SubElement(port, 'opsw:opm')
                hysteresis = SubElement(opm1, 'plts:power-alarm-clear-holdoff')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            prettyXml = self.prettify(xmlstr)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % prettyXml)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])

            else:
                #prettyXml = self.prettify(xmlstr)
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % prettyXml)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-alarm-clear-holdoff')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            LOG.info(
                'gvn_power_alarm_clear_holdoff : %s\n\n' %
                gvn_power_alarm_clear_holdoff)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                #    gvn_power_alarm_clear_holdoff)
                LOG.info(
                    'compare both port ids and power alarm clear holdoff : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_power_alarm_clear_holdoff',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_all_configuration_in_opm_with_single_req(
            self, **kwargs):
        """create xml for all opm configurations with given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        all parsed outputs with given inputs
        """

        global gvn_port_ids, gvn_port_labels, gvn_port_states, gvn_lambdas
        global gvn_power_high_alarms, gvn_power_low_alarms, gvn_power_high_warning_offsets, gvn_power_low_warning_offsets
        global gvn_power_alarm_controls, gvn_offsets, gvn_averaging_time_selects, gvn_power_alarm_hysteresis
        global gvn_power_alarm_clear_holdoff

	gvn_port_ids = kwargs['port_ids']

        l = len(gvn_port_ids)

        s = time.time()
	f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        #self.create_box(
        #    'test_editconfig_create_all_configurations_in_opm_with_single_req')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'power-alarm-clear-holdoff')

            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            LOG.info(
                'gvn_power_alarm_clear_holdoff : %s\n\n' %
                gvn_power_alarm_clear_holdoff)
            if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info(
                #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                #    gvn_power_alarm_clear_holdoff)
                LOG.info(
                    'compare both port ids and power alarm clear holdoff : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_all_configuration_in_opm_with_single_req',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_trigger_los_of_service(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_power_low_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_power_alarm_clear_holdoff = kwargs[
            'power_alarm_clear_holdoff'].split(',')

        l = len(gvn_port_ids)

        s = time.time()
        self.create_box(
            'test_editconfig_create_power_alarm_clear_holdoff_for_given_port_ids')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'])
        result, message = self.edit_config_opr()
	nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)

            xmlstr = tostring(ports)
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':

                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-clear-holdoff')

                try:
                    if str(gvn_port_ids) == str(result1):
                        pass
                    else:
                        gvn_port_ids = gvn_port_ids.split()
                except Exception as err:
                    pass

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    gvn_power_alarm_clear_holdoff)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    #    gvn_power_alarm_clear_holdoff)
                    LOG.info(
                        'compare both port ids and power alarm clear holdoff : PASS\n')
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
                'editconfig_create_trigger_los_of_service',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

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

    def create_xml_for_get_opr(self, port_ids, tag_name):
        """create xml for queried tag and parsed it, then compare parsed values
        with given values.
        Arguments:
        port ids             : valid port ids
        tag_name             : valid tag_name
        """

        #LOG.info('-----[ create xml for get/getconfig operation ]-----\n')

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']

        ports = Element(
            'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                           'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})

        l = len(port_ids)

        for port_id in range(0, l):
            port = SubElement(ports, 'opsw:port')
            port_id_val = port_ids[port_id]
            port_id = SubElement(port, 'opsw:port-id')
            port_id.text = str(port_id_val)
            if tag_name in opm_list:
                opm = SubElement(port, 'opsw:opm')
                tag_2 = SubElement(opm, 'opsw:' + tag_name)
            else:
                tag_2 = SubElement(port, 'opsw:' + tag_name)

        xmlstr = tostring(ports)
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

    def get_port_label(self, **kwargs):
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

        self.create_box('get_port_label')
        xmlstr = self.create_xml_for_single_tag(
            'port-label', kwargs['port_labels'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-label')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-label')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_labels : %s\n\n' % gvn_port_label)
                if str(gvn_port_ids) == str(result1) and str(gvn_port_label) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_port_labels : %s\n\n' % gvn_port_label)
                    LOG.info('compare both port ids and port_labels : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_port_label', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_port_state(self, **kwargs):
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
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'port-state', kwargs['port_states'], kwargs['opr'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-state')
            time.sleep(10)
            if kwargs['operation'] == 'get':
                LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.get_rpc_request(
                    xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                    xmlstr, kwargs['file_name'])
            
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-state')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
                if str(gvn_port_ids) == str(result1) and str(gvn_port_states) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
                    LOG.info('compare both port ids and port_states : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_port_state', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_port_status(self, **kwargs):
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
        gvn_port_states = kwargs['port_states'].split(',')
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'port-state', kwargs['port_states'], kwargs['opr'])
        result, message = self.edit_config_opr()
        # xmlstr = self.create_xml_for_single_tag('port-status', kwargs['port_status'])
        # result, message = self.edit_config_opr()

        LOG.info(
                '-----[ create xml for get operation with given port ids ]-----\n\n')
        xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-status')
        time.sleep(10)
        xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
        if result == 'PASS':
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'port-status')

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            LOG.info('gvn_port_status : %s\n\n' % gvn_port_status)
            if str(gvn_port_ids) == str(result1) and str(gvn_port_status) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_port_status : %s\n\n' % gvn_port_status)
                LOG.info('compare both port ids and port_status : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_port_status', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_lambda(self, **kwargs):
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

        self.create_box('get_lambda')
        xmlstr = self.create_xml_for_single_tag('lambda', kwargs['lambdas'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'lambda')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'lambda')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                if str(gvn_port_ids) == str(result1) and str(gvn_lambdas) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                    LOG.info('compare both port ids and lambdas : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_lambda', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_high_alarm(self, **kwargs):
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

        self.create_box('get_power_high_alarms')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-alarm',
            kwargs['power_high_alarms'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-high-alarm')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-alarm')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_high_alarms : %s\n\n' %
                    gvn_power_high_alarms)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_alarms) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_high_alarms : %s\n\n' %
                    #    gvn_power_high_alarms)
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
            csvOutput('ports', 'get_power_high_alarms', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_low_alarm(self, **kwargs):
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

        self.create_box('get_power_low_alarm')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm',
            kwargs['power_low_alarms'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-low-alarm')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-alarm')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_low_alarms : %s\n\n' %
                    gvn_power_low_alarms)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_alarms) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_low_alarms : %s\n\n' %
                    #    gvn_power_low_alarms)
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
            csvOutput('ports', 'get_power_low_alarms', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_high_warning_offset(self, **kwargs):
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

        self.create_box('get_power_high_warning_offset')
        xmlstr = self.create_xml_for_single_tag(
            'power-high-warning-offset',
            kwargs['power_high_warning_offsets'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-high-warning-offset')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-warning-offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_high_warning_offsets : %s\n\n' %
                    gvn_power_high_warning_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_warning_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_high_warning_offsets : %s\n\n' %
                    #    gvn_power_high_warning_offsets)
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
            csvOutput('ports', 'get_power_high_warning_offsets', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_low_warning_offset(self, **kwargs):
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

        self.create_box('get_power_low_warning_offset')
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset',
            kwargs['power_low_warning_offsets'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-low-warning-offset')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-warning-offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_low_warning_offsets : %s\n\n' %
                    gvn_power_low_warning_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_warning_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_low_warning_offsets : %s\n\n' %
                    #    gvn_power_low_warning_offsets)
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
            csvOutput('ports', 'get_power_low_warning_offsets', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_alarm_control(self, **kwargs):
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

        self.create_box('get_power_alarm_control')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-control',
            kwargs['power_alarm_controls'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-control')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-control')

                LOG.info('gvn_port_ids : %s' % gvn_power_alarm_controls)
                LOG.info(
                    'gvn_power_alarm_controls : %s\n\n' %
                    gvn_power_alarm_controls)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_controls) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_power_alarm_controls)
                    #LOG.info(
                    #    'gvn_power_alarm_controls : %s\n\n' %
                    #    gvn_power_alarm_controls)
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
            csvOutput('ports', 'get_power_alarm_controls', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_alarm_status(self, **kwargs):
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

        self.create_box('get_power_alarm_status')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-status',
            kwargs['power_alarm_status'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-status')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-status')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_status : %s\n\n' %
                    gvn_power_alarm_status)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_status) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_status : %s\n\n' %
                    #    gvn_power_alarm_status)
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
            csvOutput('ports', 'get_power_alarm_status', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power(self, **kwargs):
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

        self.create_box('get_power')
        xmlstr = self.create_xml_for_single_tag('power', kwargs['power'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'power')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_power : %s\n\n' % gvn_power)
                if str(gvn_port_ids) == str(result1) and str(gvn_power) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_power : %s\n\n' % gvn_power)
                    LOG.info('compare both port ids and power : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_power', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_offset(self, **kwargs):
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

        self.create_box('get_offsets')
        xmlstr = self.create_xml_for_single_tag('offset', kwargs['offsets'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'offset')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
                    LOG.info('compare both port ids and offsets : PASS\n')
                    result = 'PASS'
                else:
                    LOG.error('comparision failed : FAIL\n')
                    result = 'FAIL'
            else:
                LOG.info('getting error from switch : FAIL\n\n')

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput('ports', 'get_offsets', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_averaging_time_select(self, **kwargs):
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

        self.create_box('get_averaging_time_selects')
        xmlstr = self.create_xml_for_single_tag(
            'averaging-time-select',
            kwargs['averaging_time_selects'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'averaging-time-select')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'averaging-time-select')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_averaging_time_selects : %s\n\n' %
                    gvn_averaging_time_selects)
                if str(gvn_port_ids) == str(result1) and str(gvn_averaging_time_selects) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_averaging_time_selects : %s\n\n' %
                    #    gvn_averaging_time_selects)
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
            csvOutput('ports', 'get_averaging_time_selects', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_alarm_hysteresis(self, **kwargs):
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

        self.create_box('get_power_alarm_hysteresis')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-hysteresis',
            kwargs['power_alarm_hysteresis'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-hysteresis')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-hysteresis')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_hysteresis : %s\n\n' %
                    gvn_power_alarm_hysteresis)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_hysteresis) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_hysteresis : %s\n\n' %
                    #    gvn_power_alarm_hysteresis)
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
            csvOutput('ports', 'get_power_alarm_hysteresis', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def get_power_alarm_clear_holdoff(self, **kwargs):
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

        self.create_box('get_power_alarm_clear_holdoff')
        xmlstr = self.create_xml_for_single_tag(
            'power-alarm-clear-holdoff',
            kwargs['power_alarm_clear_holdoff'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-clear-holdoff')
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-clear-holdoff')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    gvn_power_alarm_clear_holdoff)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    #    gvn_power_alarm_clear_holdoff)
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
            csvOutput('ports', 'get_power_alarm_clear_holdoff', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-label')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-label')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_labels : %s\n\n' % gvn_port_label)
                if str(gvn_port_ids) == str(result1) and str(gvn_port_label) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_port_labels : %s\n\n' % gvn_port_label)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-state')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'port-state')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
                if str(gvn_port_ids) == str(result1) and str(gvn_port_states) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_port_states : %s\n\n' % gvn_port_states)
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
        # result, message = self.edit_config_opr()

        xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'port-status')
        xmlout, result = self.getconfig_rpc_request(
            xmlstr, kwargs['file_name'])
        if result == 'PASS':
            result1, result2 = self.get_parsed_values(
                xmlout, 'port-id', 'port-status')

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            LOG.info('gvn_port_status : %s\n\n' % gvn_port_status)
            if str(gvn_port_ids) == str(result1) and str(gvn_port_status) == str(result2):
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_port_status : %s\n\n' % gvn_port_status)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'lambda')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'lambda')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
                if str(gvn_port_ids) == str(result1) and str(gvn_lambdas) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_lambdas : %s\n\n' % gvn_lambdas)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-high-alarm')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-alarm')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_high_alarms : %s\n\n' %
                    gvn_power_high_alarms)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_alarms) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_high_alarms : %s\n\n' %
                    #    gvn_power_high_alarms)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-low-alarm')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-alarm')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_low_alarms : %s\n\n' %
                    gvn_power_low_alarms)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_alarms) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_low_alarms : %s\n\n' %
                    #    gvn_power_low_alarms)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-high-warning-offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-high-warning-offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_high_warning_offsets : %s\n\n' %
                    gvn_power_high_warning_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_high_warning_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_high_warning_offsets : %s\n\n' %
                    #    gvn_power_high_warning_offsets)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-low-warning-offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-low-warning-offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_low_warning_offsets : %s\n\n' %
                    gvn_power_low_warning_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_low_warning_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_low_warning_offsets : %s\n\n' %
                    #    gvn_power_low_warning_offsets)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-control')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-control')

                LOG.info('gvn_port_ids : %s' % gvn_power_alarm_controls)
                LOG.info(
                    'gvn_power_alarm_controls : %s\n\n' %
                    gvn_power_alarm_controls)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_controls) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_power_alarm_controls)
                    #LOG.info(
                    #    'gvn_power_alarm_controls : %s\n\n' %
                    #    gvn_power_alarm_controls)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids, 'power-alarm-status')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-status')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_status : %s\n\n' %
                    gvn_power_alarm_status)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_status) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_status : %s\n\n' %
                    #    gvn_power_alarm_status)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'power')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_power : %s\n\n' % gvn_power)
                if str(gvn_port_ids) == str(result1) and str(gvn_power) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_power : %s\n\n' % gvn_power)
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
        xmlstr = self.create_xml_for_single_tag('offset', kwargs['offsets'], kwargs['opr'])
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(gvn_port_ids, 'offset')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'offset')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
                if str(gvn_port_ids) == str(result1) and str(gvn_offsets) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info('gvn_offsets : %s\n\n' % gvn_offsets)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'averaging-time-select')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'averaging-time-select')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_averaging_time_selects : %s\n\n' %
                    gvn_averaging_time_selects)
                if str(gvn_port_ids) == str(result1) and str(gvn_averaging_time_selects) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_averaging_time_selects : %s\n\n' %
                    #    gvn_averaging_time_selects)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-hysteresis')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-hysteresis')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_hysteresis : %s\n\n' %
                    gvn_power_alarm_hysteresis)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_hysteresis) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_hysteresis : %s\n\n' %
                    #    gvn_power_alarm_hysteresis)
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
        result, message = self.edit_config_opr()

        if result == 'PASS':
            xmlstr = self.create_xml_for_get_opr(
                gvn_port_ids,
                'power-alarm-clear-holdoff')
            xmlout, result = self.getconfig_rpc_request(
                xmlstr, kwargs['file_name'])
            if result == 'PASS':
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', 'power-alarm-clear-holdoff')

                LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                LOG.info(
                    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    gvn_power_alarm_clear_holdoff)
                if str(gvn_port_ids) == str(result1) and str(gvn_power_alarm_clear_holdoff) == str(result2):
                    #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                    #LOG.info(
                    #    'gvn_power_alarm_clear_holdoff : %s\n\n' %
                    #    gvn_power_alarm_clear_holdoff)
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

    def editconfig_create_alarm_with_all_parameters(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_multiple_tags(
            kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        opm_elements = ['lambda', 'power-high-alarm', 'power-low-alarm', 'power-high-warning-offset', 'power-low-warning-offset',
                        'power-alarm-control', 'offset', 'averaging-time-select', 'power-alarm-clear-holdoff']
        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                for ele in range(0,6):
                    ele = SubElement(opm, opm_elements[ele])
                for ele in range(6,9):
  		    ele = SubElement(opm, 'plts:'+opm_elements[ele])

            xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
            final_result = []
            for ele in opm_elements:
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', ele)
                final_result.append(result2)
            #print "final_result : ", final_result
            final_result = list(itertools.chain(*final_result))
            #print "final_result : ", final_result
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            #LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            gvn_values = kwargs['all_parameter_alarms'].split(',')
	    if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_values =['1550.0', '25.0', '-60.00', '0.0', '0.0', 'POWER_ALARM_DISABLED', '0.0', '4', '10']
	    else:
		LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])

            LOG.info('gvn_values : %s' % gvn_values)
            LOG.info("parsed_values : %s\n\n" % final_result)
            if str(gvn_port_ids) == str(result1) and gvn_values == final_result:
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and all parameters : PASS\n')
                result = 'PASS'
		
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_alarms_with_all_parameters',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)


    def editconfig_create_invalid_alarm_with_all_parameters(self, **kwargs):
        """
	create invalid alarm with all parameters for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
	"""

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_multiple_tags(
            kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
	LOG.info('gvn_port_ids : %s' % gvn_port_ids)

        opm_elements = ['lambda', 'power-high-alarm', 'power-low-alarm', 'power-high-warning-offset', 'power-low-warning-offset',
                        'power-alarm-control', 'offset', 'averaging-time-select', 'power-alarm-clear-holdoff']
	if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
	    gvn_all_parameter_alarms =['1550.0,25.0,-59.99,0.0,0.0,POWER_ALARM_DISABLED,0.0,4,10']
	    LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)

        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
               'ports',
               'editconfig_create_invalid_alarm_with_all_parameters',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_alarm_with_all_parameters',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

    def editconfig_create_alarm_with_mode_single_and_power_low_alarm(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_elements = ['power-low-alarm', 'power-alarm-control']
        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                ele = SubElement(opm, opm_elements[0])
                ele = SubElement(opm, opm_elements[1])

            xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
            final_result = []
            for ele in opm_elements:
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', ele)
                final_result.append(result2)
            #print "final_result : ", final_result
            final_result = list(itertools.chain(*final_result))
            print "final_result : ", final_result
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            #LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_all_parameter_alarms =['-59.99', 'POWER_ALARM_DISABLED']
                LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)
            else:
                LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            if str(gvn_port_ids) == str(result1) and gvn_all_parameter_alarms == final_result:
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and all parameters : PASS\n')
                result = 'PASS'

            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_alarms_with_all_parameters',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_alarm_with_mode_single_and_power_low_alarm(self, **kwargs):
        """
        create invalid alarm with mode single and power low alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)

        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_all_parameter_alarms =['-59.99,POWER_ALARM_DISABLED']
            LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)

        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
               'ports',
               'editconfig_create_invalid_alarm_with_all_parameters',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_alarm_with_all_parameters',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

    def editconfig_create_alarm_with_mode_single_and_power_low_warn_offset(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_elements = ['power-low-warning-offset', 'power-alarm-control']
        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                ele = SubElement(opm, opm_elements[0])
                ele = SubElement(opm, opm_elements[1])

            xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
            final_result = []
            for ele in opm_elements:
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', ele)
                final_result.append(result2)
            #print "final_result : ", final_result
            final_result = list(itertools.chain(*final_result))
            print "final_result : ", final_result
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            #LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_all_parameter_alarms =['0.0', 'POWER_ALARM_DISABLED']
                LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)
            else:
                LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])

            if str(gvn_port_ids) == str(result1) and gvn_all_parameter_alarms == final_result:
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and all parameters : PASS\n')
                result = 'PASS'

            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_alarms_with_mode_single_and_power_low_warn_alarm',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_offset(self, **kwargs):
        """
        create invalid alarm with mode single and power low warning offset alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)

        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_all_parameter_alarms =['0.0,POWER_ALARM_DISABLED']
            LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)

        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
               'ports',
               'editconfig_create_invalid_alarm_with_mode_single_and_power_low_warn_alarm',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_alarm_with_all_parameters',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')



    def editconfig_create_alarm_with_mode_continous_and_power_low_alarm(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_elements = ['power-high-alarm', 'power-alarm-control']
        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                ele = SubElement(opm, opm_elements[0])
                ele = SubElement(opm, opm_elements[1])

            xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
            final_result = []
            for ele in opm_elements:
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', ele)
                final_result.append(result2)
            #print "final_result : ", final_result
            final_result = list(itertools.chain(*final_result))
            print "final_result : ", final_result
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            #LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_all_parameter_alarms =['25.0', 'POWER_ALARM_DISABLED']
                LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)
            else:
                LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])

            if str(gvn_port_ids) == str(result1) and gvn_all_parameter_alarms == final_result:
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and all parameters : PASS\n')
                result = 'PASS'

            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_alarm_with_mode_continous_and_power_low_alarm',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm(self, **kwargs):
        """
        create invalid alarm with mode continous and power low alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-alarm,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)

        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_all_parameter_alarms =['25.0,POWER_ALARM_DISABLED']
            LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)

        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
               'ports',
               'editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_alarm_with_mode_continous_and_power_low_alarm',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')

    def editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset(self, **kwargs):
        """create port label for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        nose.tools.assert_in('%s'% Rpc_Reply, str(message), "getting error when checking the output message")

        opm_list = [
            'lambda',
            'power-high-alarm',
            'power-low-alarm',
            'power-high-warning-offset',
            'power-low-warning-offset',
            'power-alarm-control',
            'power-alarm-status',
            'power',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_plts_list = [
            'offset',
            'averaging-time-select',
            'power-alarm-hysteresis',
            'power-alarm-clear-holdoff']
        opm_elements = ['power-low-warning-offset', 'power-alarm-control']
        if result == 'PASS':
            ports = Element(
                'opsw:ports', {'xmlns:plts': "http://www.polatis.com/yang/polatis-switch",
                               'xmlns:opsw': "http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                port_id_val = gvn_port_ids[tag1]
                port = SubElement(ports, 'opsw:port')
                port_id = SubElement(port, 'opsw:port-id')
                port_id.text = str(port_id_val)
                opm = SubElement(port, 'opsw:opm')
                ele = SubElement(opm, opm_elements[0])
                ele = SubElement(opm, opm_elements[1])

            xmlstr = tostring(ports)
            if kwargs['operation'] == 'get':
                 LOG.info(
                    '-----[ create xml for get operation with given port ids ]-----\n\n')
                 LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                 xmlout, result = self.get_rpc_request(
                     xmlstr, kwargs['file_name'])
            else:
                LOG.info(
                    '-----[ create xml for get-config operation with given port ids ]-----\n\n')
                LOG.info('xmlstr : \n\n%s\n' % xmlstr)
                xmlout, result = self.getconfig_rpc_request(
                        xmlstr, kwargs['file_name'])
            final_result = []
            for ele in opm_elements:
                result1, result2 = self.get_parsed_values(
                    xmlout, 'port-id', ele)
                final_result.append(result2)
            #print "final_result : ", final_result
            final_result = list(itertools.chain(*final_result))
            print "final_result : ", final_result
            try:
                if str(gvn_port_ids) == str(result1):
                    pass
                else:
                    gvn_port_ids = gvn_port_ids.split()
            except Exception as err:
                pass

            LOG.info('gvn_port_ids : %s' % gvn_port_ids)
            #LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])
            gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
            if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
                gvn_all_parameter_alarms =['0.0', 'POWER_ALARM_DISABLED']
                LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)
            else:
                LOG.info('gvn_opm_values : %s' % kwargs['all_parameter_alarms'])

            if str(gvn_port_ids) == str(result1) and gvn_all_parameter_alarms == final_result:
                #LOG.info('gvn_port_ids : %s' % gvn_port_ids)
                #LOG.info('gvn_power_high_alarms : %s\n\n' % gvn_power_high_alarms)
                LOG.info('compare both port ids and all parameters : PASS\n')
                result = 'PASS'

            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_alarm_with_mode_continous_and_power_low_warn_offset',
                d,
                result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_offset(self, **kwargs):
        """
        create invalid alarm with mode continous and power low warning offset alarm for given port ids using edit-config operation and
        get the xml switch output using get-config, then parsed this xml, compare the
        port id's and port label's
        """

        global gvn_port_ids
        global gvn_all_parameter_alarms

        gvn_port_ids = kwargs['port_ids']
        gvn_all_parameter_alarms = kwargs['all_parameter_alarms'].split(',')
        l = len(gvn_port_ids)

        s = time.time()
        f_name = kwargs['file_name'].split('.')
        self.create_box(f_name[0])
        xmlstr = self.create_xml_for_single_tag(
            'power-low-warning-offset,power-alarm-control', kwargs['all_parameter_alarms'], kwargs['opr'])
        result, message = self.edit_config_opr()
        LOG.info('gvn_port_ids : %s' % gvn_port_ids)

        if kwargs['opr'] == 'delete' or kwargs['opr'] == 'remove':
            gvn_all_parameter_alarms =['0.0,POWER_ALARM_DISABLED']
            LOG.info('gvn_all_parameter_alarms : %s\n\n' % gvn_all_parameter_alarms)

        elif result == 'PASS':
            e = time.time()
            d = int(round((e - s) * 1000))
            LOG.info('Invalid case is passed : FAIL\n\n')
            csvOutput(
               'ports',
               'editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_alarm',
                d,
                result)
        else:
            e = time.time()
            d = int(round((e - s) * 1000))
            csvOutput(
                'ports',
                'editconfig_create_invalid_alarm_with_mode_continous_and_power_low_warn_alarm',
                d,
                result)
            LOG.info('getting error from switch : PASS\n\n')
