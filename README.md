Google Summer of Code 2020 Coding exercise
==========================================


**Tasks:**

- [X] Implement functions to print the domain details like domain state, disk, allocated memory, allocated cpu's , IP address with prefix and interfaces by importing libvirt python module.

- [X] Implement daemon listening for libvirt events and displaying those informations for every newly created VM.


## Execution

  For example, if the uri and domain name like qemu:///system, CentOS7.Then run the following command to print the domain details.
   
   ```make exercise uri=qemu:///system dom_name=CentOS7```
   
## Systemd service execution
 
   Directory to the service
   
```/lib/systemd/system/libvirt-event-listener.service```

  To reload the daemon

```sudo systemctl daemon-reload```

  To start the daemon service

```sudo systemctl start libvirt-event-listener.service```
   
Thanks for reading. I am Kaviya Periyasamy. I have applied for GSoC 2020 under the organization Libvirt to work on the ‘Redfish API Implementation’ project. This repo holds the solution for the assignment given by the mentor before the interview.I can be reached at kaviyaperiyasamy22@gmail.com
