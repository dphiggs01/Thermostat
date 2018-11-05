
1. Setup ssh with keys so you don't need to login each time you connect to the pi
    * check if you already have keys. on the machine you want to connect from. (for me this is my mac) if `ls ~/.ssh` has files *id_rsa, id_rsa.pub* skip key generation step.
    * generate keys with `ssh-keygen -t rsa -C <YOURNANME>@<HOSTNAME>` replace *YOURNANME, HOSTNAME* with the use and host of your machine.
    * login to the pi and check if you have .ssh directory. `ls ~/.ssh` if not `install -d -m 700 ~/.ssh`
    * now you need to copy your public key from your host to the pi. `cat ~/.ssh/id_rsa.pub | ssh pi@<IP-ADDRESS> 'cat >> .ssh/authorized_keys'`
    * you should now have access without login. for additional info check [here](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)

2.

