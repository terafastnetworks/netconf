import sys
import time
import xml.dom.minidom
from xml.dom import minidom
from ncclient import manager
from xml.dom.minidom import parse, parseString



def writeToFile(fileName, data):

                f = open(fileName,'w')
                f.write(data)
                f.close()

def prettify(xmlstr):

        """Used for prettify the XML output from switch.
        Arguments: 
           xmlstr       : any xml string
        """

        reparsed = minidom.parseString(xmlstr)
        return reparsed.toprettyxml(indent=" ")


### get product information

def get_product_info(host, port, userName, password, timeout):

    print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)


    #product_information_Str="""<opsw:product-information xmlns:opsw="http://www.polatis.com/yang/optical-switch"/>"""
    product_information_Str="""<opsw:ports xmlns:opsw="http://www.polatis.com/yang/optical-switch"><opsw:port><opsw:port-id>1</opsw:port-id></opsw:port></opsw:ports>"""
    for session in range(0, 1):
        try:
            print "get product information..\n"
            print "product_information_Str : %s\n\n" % product_information_Str
            xmlout = swMgr.get(filter=('subtree',product_information_Str)).data_xml
            xmlout = prettify(xmlout)
            print "xmlout : %s\n\n" % xmlout
            time.sleep(5)
        except Exception as err:
            print "Error: %s" % err

### main
get_product_info('10.99.99.225','830','admin','root',60)
