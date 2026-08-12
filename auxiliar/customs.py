import os

def orchestrate(nodes_dict, duration):
    """ 
    Insert custom orchestration here.
    Nodes are called via nodes_dict['node_name']. Use the .cmd method to call bash commands.
    e.g.: nodes_dict['h1'].cmd(f"bash -c 'scripts/custom-script.sh {duration}'")
    """
    h1, h2 = nodes_dict['h1'], nodes_dict['h2']
    s2 = nodes_dict['s2']
    h1.cmd("arp -s 10.0.0.2 00:00:00:00:02:02")
    h2.cmd("arp -s 10.0.0.1 00:00:00:00:01:01")

    h1.cmd("ethtool -K h1-eth0 tx off rx off")
    h2.cmd("ethtool -K h2-eth0 tx off rx off")

    s2.cmd("ip link set s2-eth0 up")
    s2.cmd("ip link set s2-eth1 up")
    s2.cmd("tcpdump -i s2-eth0 -s0 -w /tmp/dump-bmv2-$(date +'%Y%m%d_%H%M%S').pcap &")

    s2.cmd('cat /tmp/compile/ipv4lpm.txt | simple_switch_CLI')
    s2.cmd('cat /tmp/compile/table.txt | simple_switch_CLI')

    h2.cmd("service vsftpd start; iperf3 -sD; nginx -g 'daemon off;' &")
    h1.cmd("tcpdump -i h1-eth0 -s0 -w /tmp/dump-$(date +'%Y%m%d_%H%M%S').pcap &")
    h1.cmd(f"scripts/consume.sh {duration} &")

    return
