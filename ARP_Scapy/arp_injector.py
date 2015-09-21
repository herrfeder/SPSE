import socket
import struct

#IP Packet
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

#sniffing raw packets. Binding to interface
rawSocket.bind(("wlan0", socket.htons(0x0800)))

#sending ARP Packet
packet=struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s",'\xFF\xFF\xFF\xFF\xFF\xFF','\x00\x0c\x29\x3c\x06\x5c', '\x08\x06', '\x00\x01', '\x08\x00', '\x06', '\x04', '\x00\x01', '\x00\x0c\x29\x3c\x06\x5c', socket.inet_aton('192.168.159.132'), '\x00\x00\x00\x00\x00\x00', socket.inet_aton('192.168.212.1'))

# Destination-MAC-Address::Source-MAC-Address::Type-Of-Ethernet(0806)::Hardware-Type(0001)::ARP-Protocol-Type(0800)::Hardware-Size(06)::Protocol-Size(04)::OpCode(0010 = Request)::Sender-MAC-Address::Sender-IP-Address::Target-MAC-Address::Target-IP-Address

rawSocket.send(packet)
