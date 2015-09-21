#!/usr/bin/env python2.7

import plac
import random
import string
import sys

import scapy
import scapy.main
scapy.config.conf.logLevel = 40
from scapy.all import *

## Items needed to randomly generate domains
tlds=(
'AC','AD','AE','AERO','AF','AG','AI','AL','AM','AN','AO','AQ','AR','ARPA',
'AS','ASIA','AT','AU','AW','AX','AZ','BA','BB','BD','BE','BF','BG','BH',
'BI','BIZ','BJ','BM','BN','BO','BR','BS','BT','BV','BW','BY','BZ','CA','CAT',
'CC','CD','CF','CG','CH','CI','CK','CL','CM','CN','CO','COM','COOP','CR','CU',
'CV','CW','CX','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EDU','EE','EG',
'ER','ES','ET','EU','FI','FJ','FK','FM','FO','FR','GA','GB','GD','GE','GF','GG',
'GH','GI','GL','GM','GN','GOV','GP','GQ','GR','GS','GT','GU','GW','GY','HK',
'HM','HN','HR','HT','HU','ID','IE','IL','IM','IN','INFO','INT','IO','IQ','IR',
'IS','IT','JE','JM','JO','JOBS','JP','KE','KG','KH','KI','KM','KN','KP','KR',
'KW','KY','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC',
'MD','ME','MG','MH','MIL','MK','ML','MM','MN','MO','MOBI','MP','MQ','MR','MS',
'MT','MU','MUSEUM','MV','MW','MX','MY','MZ','NA','NAME','NC','NE','NET','NF',
'NG','NI','NL','NO','NP','NR','NU','NZ','OM','ORG','PA','PE','PF','PG','PH',
'PK','PL','PM','PN','POST','PR','PRO','PS','PT','PW','PY','QA','RE','RO','RS',
'RU','RW','SA','SB','SC','SD','SE','SG','SH','SI','SJ','SK','SL','SM','SN','SO',
'SR','ST','SU','SV','SX','SY','SZ','TC','TD','TEL','TF','TG','TH','TJ','TK',
'TL','TM','TN','TO','TP','TR','TRAVEL','TT','TV','TW','TZ','UA','UG','UK','US',
'UY','UZ','VA','VC','VE','VG','VI','VN','VU','WF','WS','XXX','YE','YT','ZA',
'ZM','ZW'
)

num_digits = random.randint(1, 8)
num_upper = random.randint(1, 8)
num_lower = random.randint(1, 8)
default_tld = random.choice(tlds)

## Generate a random domain
def get_domain(num_d, num_u, num_l, tld):
    domain = []

    for i in range(1, num_d+1):
        domain.append(str(random.randint(0, 9)))

    for i in range(1, num_u+1):
        domain.append(random.choice(string.ascii_uppercase))

    for i in range(1, num_l+1):
        domain.append(random.choice(string.ascii_lowercase))

    random.shuffle(domain)
    domain = "{0}.{1}".format("".join(domain), tld.lower())

    return domain


## Program options configuration
@plac.annotations(
    iface=("Interface to use", "option", "i", str),
    dst=("Destination IP", "option", None, str),
    src=("Source IP", "option", None , str),
    sport=("Source port", "option", None, int),
    dport=("Destination port", "option", None, int),
    id=("DNS ID", "option", None, int),
    qr=("QR", "option", None, int),
    opcode=("Opcode", "option", None, int),
    aa=("AA", "option", None, int),
    tc=("TC", "option", None, int),
    rd=("RD", "option", None, int),
    ra=("RA", "option", None, int),
    z=("Z", "option", None, int),
    rcode=("Rcode", "option", None, int),
    qname=("Domain", "option", None, str),
    qtype=("Query type", "option", None, int),
    qclass=("Query class", "option", None, int),

    ## If these are not provided, domain is randomly-generated binary
    numd=("Number of digits for domain", "option", None, int),
    numu=("Number of uppers for domain", "option", None, int),
    numl=("Number of lowers for domain", "option", None, int),
    tld=("Static TLD to use for domain", "option", None, str),
)
def main(iface=None, dst='127.0.0.1', src='127.0.0.1', sport=None, dport=53, 
        id=None, qr=None, opcode=None, aa=None, tc=None, rd=None, ra=None,
        z=None, rcode=None, qname=None, qtype=None, qclass=None, numd=None,
        numu=None, numl=None, tld=None):

    dns_fuzz_fields = ('id', 'qr', 'opcode', 'aa', 'tc', 'rd', 'ra', 'z', 'rcode')
    l = locals()

    if numd is not None or numu is not None or numl is not None or tld is not None:
        if numd is None: numd = num_digits
        if numu is None: numu = num_upper
        if numl is None: numl = num_lower
        if tld is None:
            tld = default_tld
        else:
            tld = tld.lstrip('.')

        qname = get_domain(numd, numu, numl, tld)

    ip_p = IP()
    udp_p = UDP()
    dns_p = DNS()
    dns_qd = DNSQR()

    if iface is None: iface = scapy.config.conf.iface
    if src is not None: ip_p.src = src
    if dst is not None: ip_p.dst = dst
    if sport is not None: udp_p.sport = sport
    if dport is not None: udp_p.dport = dport

    for field in dns_fuzz_fields:
        if l[field] is not None:
            dns_p.setfieldval(field, l[field])

    if qname is not None: dns_qd.qname = qname
    if qtype is not None: dns_qd.qtype = qtype
    if qclass is not None: dns_qd.qclass = qclass

    dns_p.qd = fuzz(dns_qd)
    pkt = ip_p/udp_p/fuzz(dns_p)

    ans = sr1(pkt)
    print ans.show()


if __name__ == '__main__':
    parser = plac.parser_from(main)
    sys.exit(plac.call(main))

