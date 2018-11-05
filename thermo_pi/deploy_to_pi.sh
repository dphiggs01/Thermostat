#!/usr/bin/env bash
if [ "$1" == "" ]; then
    echo no pi address passed! usage deploy_to_pi.sh pi@192.168.1.33
    exit
else
    cd /Users/danhiggins/Code/Python/pi
    tar -cvf thermo_pi.tar thermo_pi
    scp thermo_pi.tar $1:/home/pi/Applications
    ssh $1 'cd /home/pi/Applications; rm -rf thermo_pi'
    ssh $1 'cd /home/pi/Applications; tar -xvf thermo_pi.tar'
#    ssh $1 'cd /home/pi/Applications/thermo_pi; ./run_pi.sh'
fi

