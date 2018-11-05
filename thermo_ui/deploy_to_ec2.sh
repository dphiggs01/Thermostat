#!/usr/bin/env bash
PEM_KEY=/Users/danhiggins/Code/AWS/keys/Tomcat-key.pem

if [ "$1" == "" ]; then
    echo no ec2 address passed! usage deploy_to_ec2.sh ubuntu@34.206.176.170
    exit
else
    cd /Users/danhiggins/Code/Python/pi
    tar -cvf thermo_ui.tar thermo_ui
    scp -i ${PEM_KEY} thermo_ui.tar ${1}:/home/ubuntu/Applications/
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications/thermo_ui; kill -9 `cat gunicorn.pid`'|| :
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications; rm -rf thermo_ui'|| :
    ssh -i ${PEM_KEY} $1 'cd /home/ubuntu/Applications; tar -xvf thermo_ui.tar'
fi

