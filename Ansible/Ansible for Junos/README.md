

* Ansible
* Python Version : 2.6

* Usage:

0. please create a directory "Config_Saved" under Base_config

1. Collecting equip config
[root@Kwangs Base_config]# ansible-playbook main.yml

2. Seting/Deleting config
[root@Kwangs Set_config]# ansible-playbook main.yml 


* To notice


1.pleae modify it properly host ip & id & password in /etc/ansible/hosts
  Also, please change ip-addr, NTP ip, DNS ip in yml, please modify it properly.

MX960         ansible_connection=local junos_host=172.27.27.27 juniper_user=juniper  juniper_passwd=juniper port=830
T4000         ansible_connection=local junos_host=172.27.27.27 juniper_user=juniper  juniper_passwd=juniper port=830

2. please enable ssh&netconfig ssh in your router.

juniper@juniper# show system services 
ftp;
ssh;
telnet;
netconf {
    ssh;
}



* Tree

[root@Kwangs Config_collect_set]# tree
.
├── Base_config
│   ├── Config_Saved  <===== please create a directory "Config_Saved", you can also remove this after modifying main.yml
│   └── main.yml
|
└── Set_config
    ├── group_vars
    │   └── all
    └── main.yml

* Ansible hosts

[root@Kwangs Config_collect_set]# cat /etc/ansible/hosts 
[My_Control:children]
T-series
MX-series


[MX-series]
MX960         ansible_connection=local junos_host=172.27.27.27 juniper_user=juniper  juniper_passwd=juniper port=830  # please add user id/password properly.

[T-series]
T4000        ansible_connection=local junos_host=172.27.27.27 juniper_user=juniper  juniper_passwd=juniper port=830 # please add user id/password properly.

