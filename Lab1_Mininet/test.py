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

       # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )

def perfTest():
    "Create network and rum simple performance test"
    topo=MyTopo()
    net=Mininet(topo=topo,link=TCLink,controller=None)
    net.addController('floodlight',controller=RemoteController,ip='127.0.0.1')
    net.start() #Start Mininet
    print('Dumping host connections')
    dumpNodeConnections(net.hosts)
    print('Testing network connectivity')
    net.pingAll()   #Do pingall test
    # print('Test bandwidth between h1 and h2')
    # h1,h2=net.get('h1','h2')    #Get nodes by name
    # net.iperf((h1,h2))  #Do iperf test
    net.stop()  #stop Mininet

if __name__=='__main__':
    #Set log level (info, warning, critical, error, debug, output)
    setLogLevel('info')
    perfTest()




