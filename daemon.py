#!/usr/bin/python

import libvirt
import sys

# virDomainEventType is emitted during domain lifecycles (see libvirt.h)
VIR_DOMAIN_EVENT_MAPPING = {
    0: "VIR_DOMAIN_EVENT_DEFINED",
    1: "VIR_DOMAIN_EVENT_UNDEFINED",
    2: "VIR_DOMAIN_EVENT_STARTED",
    3: "VIR_DOMAIN_EVENT_SUSPENDED",
    4: "VIR_DOMAIN_EVENT_RESUMED",
    5: "VIR_DOMAIN_EVENT_STOPPED",
    6: "VIR_DOMAIN_EVENT_SHUTDOWN",
    7: "VIR_DOMAIN_EVENT_PMSUSPENDED",
}

# virDomainState
VIR_DOMAIN_STATE_MAPPING = {
    0: "VIR_DOMAIN_NOSTATE",
    1: "VIR_DOMAIN_RUNNING",
    2: "VIR_DOMAIN_BLOCKED",
    3: "VIR_DOMAIN_PAUSED",
    4: "VIR_DOMAIN_SHUTDOWN",
    5: "VIR_DOMAIN_SHUTOFF",
    6: "VIR_DOMAIN_CRASHED",
    7: "VIR_DOMAIN_PMSUSPENDED",
}

libvirt.virEventRegisterDefaultImpl()


def event_lifecycle_cb(conn, dom, event, detail, opaque):
    print("")
    print("=-" * 25)
    print("%s: event: %s (%s)" % (dom.name(), VIR_DOMAIN_EVENT_MAPPING.get(event, "?"), event))
    print("%s: state: %s (%s)" % (dom.name(), VIR_DOMAIN_STATE_MAPPING.get(dom.state()[0], "?"), dom.state()[0]))
    print("=-" * 25)


def conn_register_event_id_lifecycle(conn):
    conn.domainEventRegisterAny(
        None,
        libvirt.VIR_DOMAIN_EVENT_ID_LIFECYCLE,
        event_lifecycle_cb,
        conn)

# setup connection
conn=libvirt.open("qemu:///system")

if conn == None:
    print('Failed to open connection')
    sys.exit(1)

# register events
conn_register_event_id_lifecycle(conn)

# event loop
while True:
    libvirt.virEventRunDefaultImpl()


sys.exit(0)