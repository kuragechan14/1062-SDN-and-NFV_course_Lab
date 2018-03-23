#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class MyTopo( Topo ):
    def __init__( self ):
        Topo.__init__( self )
        host = []
        switch = []

        for i in range(1,17):
            temp = self.addHost( 'h' + str(i) )
            host.append( temp )

        for i in range(1, 21):
            temp = self.addSwitch( 's' + str(i) )
            switch.append( temp )

        # link host to switch
        for i in range(0, 16):
            self.addLink( host[i], switch[i/2], bw=100 )
        # link the edge, aggregation and core switches
        for i in range(0, 8):
            self.addLink( switch[i], switch[i+8], bw=100 )
            if (i % 2) == 0 :
                self.addLink( switch[i], switch[i+9], bw=100 )
                self.addLink( switch[i+8], switch[16], bw=1000, loss=2 )
                self.addLink( switch[i+8], switch[17], bw=1000, loss=2 )
            else:
                self.addLink( switch[i], switch[i+7], bw=100 )
                self.addLink( switch[i+8], switch[18], bw=1000, loss=2 )
                self.addLink( switch[i+8], switch[19], bw=1000, loss=2 )

def perfTest():
    topo = MyTopo()
    net = Mininet( topo=topo, link=TCLink, controller=None )
    net.addController( "c0", controller=RemoteController, ip="127.0.0.1" )
    net.start()
    print "Dumping host connections"
    dumpNodeConnections( net.hosts )
    print "Testing network connectivity"
    net.pingFull()
    print "Testing bandwidth between h1 and h2"
    h2, h3, h13 = net.get( 'h2', 'h3', 'h13' )

    h2.cmdPrint( 'iperf -s -u -D -i 1' )
    h13.popen( 'iperf -s -u -i 1 > 0556045_h13_report', shell=True )
    h3.cmdPrint( 'iperf -c ' + h2.IP() + ' -u -t 10 -i 1 -b 100m' + ' > 0556045_h3_connect_pod0_report' )
    h3.cmdPrint( 'iperf -c ' + h13.IP() + ' -u -t 10 -i 1 -b 100m' + ' > 0556045_h3_connect_pod3_report' )
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
