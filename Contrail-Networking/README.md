## Intro

 Cloud is a big wave, being used here and there.
 Someone may feel hard to catch it up.
 So, let's start it from the scratch with me with fun.
 If you have any idea or comment, feel free to contact me (s99225078@gmail.com)


## What we are going to do

 By studing Contrail-Networking, which is one of Juniper Networks SDN solution as Private Cloud, 
 we would get to know Cloud.

 https://www.juniper.net/documentation/en_US/contrail19/topics/concept/understanding-contrail-networking-components.html
![contrail-networking](https://user-images.githubusercontent.com/33049747/111874212-79d66600-89d7-11eb-8f9f-36dec17b4e76.png)

 ### What i am going to post below as a series.
   1. How to install Contrail-Networking v2005 + CentOS7.7
   2. Lab tests based on 5 scienario easy step by step.
   3. How to install RedHat Open Stack13 + contrail v2005
   4. Docker network.
   5. Finding contrail vRouter NextHop  
   6. Common issues and Tips for troubleshooting in Contrail.


 ### 1. "How to install Contrail v2005 + CentOS7.7"
    
   * Lab Envrionment  
   1. Contrail v2005 , CentOS7.7
   2. The number of servers : 5
      - 4 physical servers, 1 VM on ESXI server.
   3. Lab Device
      - MX960, QFX5100     

 ### 2. "Lab tests based on 5 scienario easy step by step."

   * The number of Lab tests : 5
   1. Lab test #1 : Creating 2 VMs and the same VNs (Virtual Network) 
   2. Lab test #2 : Creating 2 VMs and different VNs (Virtual Network)
   3. Lab test #3 : Central Routing for different VNs (Virtual Network) 
   4. Lab test #4 : Ping to Internet and Ping between VMs (L3 Gateway) 
   5. Lab test #5 : Ping to Internet (Spine & leaf) 

 ### 3. "Finding Contrail vRouter Nexthop"

   1. Basic concept of vRouter next-hop & command lists
   2. Finding vRouter NH in lab#1 : L2 switching (family bridge)
   3. Finding vRouter NH in lab#4 (L3 traffic to internet)