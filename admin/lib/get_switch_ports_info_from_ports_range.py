from config import get_config_arg


def get_valid_ingress_port():
        """get the existing ingress list from config.txt file
        """
        ingress_port = []
        ex_ingress_ports = []

        ingressPrtRange = (
            get_config_arg(
                "cross_connects",
                "ingress_ports_range")).split(
                '-')

        for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1]) + 1):
            ex_ingress_ports.append(i)

        final_ing_prt_list = []

        for i in range(0, 3):
            prt_num = ex_ingress_ports[i]
            ingress_port.append(str(prt_num))
        return ingress_port


def get_valid_egress_port():
        """get the existing egress port list from config.txt file
        """
        egress_port = []
        ex_egress_ports = []

        egressPrtRange = (
            get_config_arg(
                "cross_connects",
                "egress_ports_range")).split(
                        '-')

        for j in range(int(egressPrtRange[0]), int(egressPrtRange[1]) + 1):
            ex_egress_ports.append(j)

        final_eg_prt_list = []

        for i in range(0, 3):
            prt_num = ex_egress_ports[i]
            egress_port.append(str(prt_num))
        return egress_port



def get_valid_ports():
        """get the existing egress port list from config.txt file
        """
        ports = []
        ex_ports = []

        PrtRange = (
            get_config_arg(
                "cross_connects",
                "egress_ports_range")).split(
                        '-')
        final_prts_list = []
        ing = get_valid_egress_port()
        egr = get_valid_ingress_port()
        final_prts_list.append(ing[0])
        final_prts_list.append(egr[0])
        final_prts_list.append((str(int(PrtRange[1]))))
        return final_prts_list
   
        #if switch_type == 'PSS':
        #    
        #    for j in range(int(PrtRange[0]), int(PrtRange[1]) + 1):
        #        ex_ports.append(j)
        #else:
        #    for j in range(int(PrtRange[0]), 2*(int(PrtRange[1])) + 1):
        #        ex_ports.append(j)

        #    final_prts_list = []

        #    for i in range(0, 2*(int(PrtRange[1])) - 1, int(PrtRange[1])-1):
        #        prt_num = ex_ports[i]
        #        ports.append(str(prt_num))
        #    return ports
