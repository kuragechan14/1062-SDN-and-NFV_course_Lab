#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        switch_core=[]
        switch_aggr=[]
        switch_edge=[]
        host=[]

        # Add hosts and switches
        for c in range(4):
            c_tmp=self.addSwitch('s'+str(c+1))   # 4 core switches
            switch_core.append(c_tmp)
        for a in range(8):
            a_tmp=self.addSwitch('s'+str(a+5))   # 8 aggr switches
            switch_aggr.append(a_tmp)
            if (a%2)==0:
                self.addLink(switch_core[0],a_tmp,bw=1000,loss=2)
                self.addLink(switch_core[1],a_tmp,bw=1000,loss=2)   #Link aggr to core
            else:
                self.addLink(switch_core[2],a_tmp,bw=1000,loss=2)
                self.addLink(switch_core[3],a_tmp,bw=1000,loss=2)
        for e in range(8):
            e_tmp=self.addSwitch('s'+str(e+13))   # 8 edge switches
            switch_edge.append(e_tmp)
            self.addLink(switch_aggr[e],e_tmp,bw=100)
            if (e%2)==0:
                self.addLink(switch_aggr[e+1],e_tmp,bw=100)     #Link edge to aggr
            else:
                self.addLink(switch_aggr[e-1],e_tmp,bw=100)
            for h in range(2):
                h_tmp=self.addHost('h'+str((2*e)+h+1))
                host.append(h_tmp)
                self.addLink(e_tmp,h_tmp,bw=100)   #Link host to edge

def perfTest():
    "Create network and rum simple performance test"
    topo=MyTopo()
    net=Mininet(topo=topo,link=TCLink,controller=None)
    net.addController('c0',controller=RemoteController,ip='127.0.0.1',port=6653)
    net.start() #Start Mininet
    print('Dumping host connections')
    dumpNodeConnections(net.hosts)
    print('Testing network connectivity')
    net.pingFull()   #Do pingFull
    # print('Test bandwidth between h1 and h2')
    h1,h2,h15=net.get('h1','h2','h15')    #Get nodes by name
    h1.cmdPrint('iperf -s -u -D -i 1')     #pod 0: h1 server
    #h15.cmdPrint('iperf -s -u -i 1')    #pod 3: h15 server
    #h1.popen('iperf -s -u -i 1'+' > 0656526_pod0_server_report',shell=True)
    h15.popen('iperf -s -u -i 1'+' > 0656526_pod3_server_report',shell=True)
    h2.cmdPrint('iperf -c '+h1.IP()+' -u -t 10 -i 1 -b 100m'+ ' > 0656526_pod0_connect_report')   #pod 0: h2 client
    h2.cmdPrint('iperf -c '+h15.IP()+' -u -t 10 -i 1 -b 100m'+ ' > 0656526_pod3_connect_report')

    net.stop()  #stop Mininet

if __name__=='__main__':
    #Set log level (info, warning, critical, error, debug, output)
    setLogLevel('info')
    perfTest()




