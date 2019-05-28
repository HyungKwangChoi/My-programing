PATH=$PATH:/bin:/usr/bin:/usr/sbin
while [ : ]
do
Idle_CPU=`/usr/sbin/cli -c "show chassis routing-engine" | grep Idle |awk '{print $2}'`
if [ 20 -gt $Idle_CPU ]; then
   cli -c 'show system uptime | grep "Current time:"' >> /var/log/cpu_log.txt
   cli -c "show chassis routing-engine | grep user" >> /var/log/cpu_log.txt
   cli -c "show system uptime | grep Current" >> /var/log/cpu_log.txt
   cli -c "show system processes extensive" >> /var/log/cpu_log.txt
   cli -c "show task memory detail | no-more" >> /var/log/cpu_log.txt
   cli -c "show task memory summary" >> /var/log/cpu_log.txt
   cli -c "show krt queue" >> /var/log/cpu_log.txt
   cli -c "set task accounting on"
   cli -c "show task accounting detail" >>/var/log/cpu_log.txt
   cli -c "show task accounting detail" >>/var/log/cpu_log.txt
   cli -c "show task accounting detail" >>/var/log/cpu_log.txt
        cli -c "set task accounting off"
fi
sleep 30
done