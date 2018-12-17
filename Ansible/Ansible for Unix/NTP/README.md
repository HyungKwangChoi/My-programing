
* description:
  This is to set/sync with NTP server among Unix system.

* Module:
  copy, command, shell

* Topo: 

[root@Kwangs ntp]# tree
.
├── chkconfig.log
├── group_vars
│   └── all
├── hosts
├── main.retry
├── main.yml
├── README.md
└── roles
    └── common
        ├── handlers
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        └── templates
            ├── ntp.conf
            └── resolv.conf

* Usage:
[root@Kwangs ntp]# ansible-playbook main.yml -i hosts 

