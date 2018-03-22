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

        CoreSwitch=[]
        AggrSwitch=[]
        EdgeSwitch=[]
        Host=[]

        # Add hosts and switches
        for c in range(4):
            c_tmp=self.addSwitch('c%s'%(c+1))   # 4 core switches
            CoreSwitch.append(c_tmp)
        for a in range(8):
            a_tmp=self.addSwitch('a%s'%(a+1))   # 8 aggr switches
            AggrSwitch.append(a_tmp)
            if (a%2)==0:
                self.addLink(CoreSwitch[0],a_tmp,bw=1000,loss=2)
                self.addLink(CoreSwitch[1],a_tmp,bw=1000,loss=2)   #Link aggr to core
            else:
                self.addLink(CoreSwitch[2],a_tmp,bw=1000,loss=2)
                self.addLink(CoreSwitch[3],a_tmp,bw=1000,loss=2)
        for e in range(8):
            e_tmp=self.addSwitch('e%s'%(e+1))   # 8 edge switches
            EdgeSwitch.append(e_tmp)
            self.addLink(AggrSwitch[e],e_tmp,bw=100)
            if (e%2)==0:
                self.addLink(AggrSwitch[e+1],e_tmp,bw=100)     #Link edge to aggr
            else:
                self.addLink(AggrSwitch[e-1],e_tmp,bw=100)
            for h in range(2):
                h_tmp=self.addHost('h%s'%((2*e)+h+1))
                Host.append(h_tmp)
                self.addLink(e_tmp,h_tmp,bw=100)   #Link host to edge

def perfTest():
    "Create network and rum simple performance test"
    topo=MyTopo()
    net=Mininet(topo=topo,link=TCLink,controller=None)
    net.addController('floodlight',controller=RemoteController,ip='127.0.0.1')
    net.start() #Start Mininet
    print('Dumping host connections')
    dumpNodeConnections(net.hosts)
    print('Testing network connectivity')
    net.pingFull()   #Do pingFull
    # print('Test bandwidth between h1 and h2')
    h1,h2,h15=net.get('h1','h2','h15')    #Get nodes by name
    h1.cmdPrint('iperf -s -u -I 1')     #pod 0: h1 server
    h15.cmdPrint('iperf -s -u -I 1')    #pod 3: h15 server
    h1.popen('iperf -s -u -I 1'+' > 0656526_pod0_server_report',shell=True)
    h15.popen('iperf -s -u -I 1'+' > 0656526_pod3_server_report',shell=True)
    h2.cmdPrint('iperf -c '+h1.IP()+' -u -t 10 -I 1 -b 100m'+ ' > 0656526_pod0_connect_report')   #pod 0: h2 client
    h2.cmdPrint('iperf -c '+h15.IP()+' -u -t 10 -I 1 -b 100m'+ ' > 0656526_pod3_connect_report')

    net.stop()  #stop Mininet

if __name__=='__main__':
    #Set log level (info, warning, critical, error, debug, output)
    setLogLevel('info')
    perfTest()




