from __future__ import print_function
import sys
import libvirt
from xml.etree import ElementTree
from xml.dom import minidom

'''
 * Basic domain information
 *
 * This program fetches and prints out some information for given domain.
 *   By invoking the below function:
 *   get_domain_details('qemu:///system', 'CentOS7')
 *
 *   Example info:
 *   Domain name:            test
 *   Domain state:           running
 *   Domain disks:           vda, vdb
 *   Domain interfaces:      vnet0
 *   Domain IP addresses:    192.168.122.2/24
 *
 * The first argument for the function is connection URI, the second argument is
 * domain name.
 '''

# Get the corresponding domain state
def get_domain_state(state):

    DOMAIN_STATES = {
        libvirt.VIR_DOMAIN_RUNNING:     "Running",
        libvirt.VIR_DOMAIN_BLOCKED:     "Idle",
        libvirt.VIR_DOMAIN_PAUSED:      "Paused",
        libvirt.VIR_DOMAIN_SHUTDOWN:    "Shutdown",
        libvirt.VIR_DOMAIN_SHUTOFF:     "Shut Off",
        libvirt.VIR_DOMAIN_CRASHED:     "Crashed",
        libvirt.VIR_DOMAIN_NOSTATE:     "No State",
        libvirt.VIR_DOMAIN_PMSUSPENDED: "PM Suspended"
    }
    if DOMAIN_STATES[state]:
        return f'Domain state: {DOMAIN_STATES[state]}'
    else:
        return f'Unknown domain state detected'

# Get the domain interface, ip and prefix
def get_domain_iface_ip(dom):

    ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
    for (name, val) in ifaces.iteritems():
        if val['addrs']:
            return f'Domain interface: {name}\nDomain IP: {val["addrs"]["addr"]}/{val["addrs"]["prefix"]}'
        else:
            return f'Domain interface: {name}\nDomain IP not found'

# Get the domain disk devices
def get_domain_disk(dom, type):
    devices = []

    # Create a XML tree from the domain XML description.
    tree = ElementTree.fromstring(dom.XMLDesc(0))

    for target in tree.findall("devices/%s/target" % type):
        dev = target.get("dev")
        if dev not in devices:
            devices.append(dev)

    return 'Domain disks: '+' '.join(devices)

# Fetch all the domain details
def get_domain_details(argv):

    uri=argv[1]
    dom_name=argv[2]
    conn = libvirt.open(uri)

    if conn == None:
        print(f'Failed to open connection to {uri}', file=sys.stderr)
        exit(1)

    dom = conn.lookupByName(dom_name)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        exit(1)
    
    print(f'Domain name: {dom_name}')
    print(get_domain_state(dom.info()[0]))
    print(f'The allocated memory: {dom.info()[1] / (1024*1024)}')
    print(f'The allocated cpu: {dom.info()[3]}')
    print(get_domain_iface_ip(dom))
    print(get_domain_disk(dom, 'disk'))
    conn.close()
    exit(0)

if __name__ == "__main__":
    get_domain_details(sys.argv)