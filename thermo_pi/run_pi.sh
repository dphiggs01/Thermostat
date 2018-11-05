#!/bin/bash
export PYTHONPATH=/home/pi/Applications/thermo_pi

for d in `ps auxww|grep listener_updater|cut -d' ' -f8`;do kill -9 $d;done

cd /home/pi/Applications/thermo_pi
python3.5 thermo_pi/listener_updater.py