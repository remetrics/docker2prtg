# docker2prtg.py

Python script to get stats for docker containers in a PRTG compatible sensor format (xml)

# Installation: 

Run the below two commands to install package requirements:

`sudo -i`

`apt update && apt install python3-pip && pip3 install pandas jinja2 && cp docker2prtg.py /usr/bin/docker2prtg.py && chmod +x /usr/bin/docker2prtg.py`
 
Adapt path to docker binary. You can find out the correct path by typing "which docker"

Run with docker2prtg.py `field`
