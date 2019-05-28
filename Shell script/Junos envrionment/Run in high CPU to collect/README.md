* Using a Script to Capture data When CPU is High

Please follow the procedure given below to start the script.

1. login to the router shell as root, and enter root password when prompt.
> start shell user root 

2. Create the log file (cpu_log ) under /var.log directory
touch /var/log/ cpu_log.txt

3. Change directory to /var/db/scripts/   
> % cd /var/db/scripts/

4. Type vi cpu.sh ( VI text editor for file cpu.sh)

5. Paste the above shell script then write the file and quite vi. 
For run the script:

6. Enter the following command under root shell 
nohup sh /var/db/scripts/cpu.sh &

Once the script is running, it will append the outputs to /var/log/cpu_log.txt automatically when the CPU spike happened.

==========================================================================================================================
The script contents:

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

