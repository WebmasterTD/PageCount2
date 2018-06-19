# PageCount2
Works with Konica Minolta Bizhub C280 and RaspberryPi
Displays the information in a webpage with Flask and Gunicorn.
## Installation
### 1. Raspberry init
	sudo apt-get update && sudo apt-get upgrade -y
	sudo raspi-config
		- expand filesystem
		- change password
		- enable ssh
		- terminal autologin

### 2. Static IP

	sudo nano /etc/dhcpcd.conf
		- interface eth0
		- static ip_address=192.168.1.111/24
		- static routers=192.168.1.1
		- static domain_name_servers=192.168.1.1

### 3. Dependency install
	sudo apt-get install chromium-browser x11-xserver-utils unclutter  libsnmp-dev snmp-mibs-downloader  gcc python-dev python3-dev python3-venv -y

### 4. X-server install
	sudo apt-get --no-install-recommends install xserver-xorg xserver-xorg-video-fbdev xinit

### 5. Clone repo / Create VirtualEnv
	mkdir PageCount2
	cd PageCount2
	git init
	git git remote add origin https://github.com/WebmasterTD/PageCount2
	git pull origin master

	python3 -m venv VirtualEnv
	source VirtualEnv/bin/activate
	pip install -r requrements.txt

### 6. Add to services
	sudo nano /etc/systemd/system/pagecount.service

```
[Unit]
Description=Gunicorn instance to serve pagecount
After=network.target

[Service]
User=pi
Group=pi
WorkingDirectory=/home/pi/PageCount2
Environment="PATH=/home/pi/PageCount2/VirtualEnv/bin"
ExecStart=/home/pi/PageCount2/VirtualEnv/bin/gunicorn --worker-class gevent --timeout 90  --bind 0.0.0.0:8000 wsgi -–workers 2

[Install]
WantedBy=multi-user.target
```

	sudo systemctl enable pagecount
	sudo systemctl start pagecount

### 7. Add to startup
	sudo nano /etc/rc.local

```bash
startx /usr/bin/chromium-browser --kiosk 0.0.0.0:8000 --incognito --window-size=1920,1080 --no-sandbox --noerrdialogs
python /home/pi/off_switch.py
```
