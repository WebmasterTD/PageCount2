# PageCount2
Works with Konica Minolta Bizhub C280 and RaspberryPi
Displays the information in a webpage with Flask and Gunicorn.
## Installation

1. sudo apt-get update && sudo apt-get upgrade -y
2. sudo raspi-config
		expand filesystem
		change pass >>> konicaminolta
		enable ssh
		terminal autologin
	
	3. sudo nano /etc/dhcpcd.conf

		interface eth0
		static ip_address=192.168.1.111/24
		static routers=192.168.1.1
		static domain_name_servers=192.168.1.1

	4. sudo apt-get install chromium-browser x11-xserver-utils unclutter  libsnmp-dev snmp-mibs-downloader  gcc python-dev python3-dev python3-venv -y

	5. sudo apt-get --no-install-recommends install xserver-xorg xserver-xorg-video-fbdev xinit

	6.
ls -l /dev/disk/by-uuid/
sudo mkdir /media/usb
sudo chown -R pi:pi /media/usb
sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi

cp PageCount2 /home/pi/PageCount2
cd PageCount2
python3 -m venv VirtualEnvst
source VirtualEnv/bin/activate

pip install -r requrements.txt

	7.
sudo nano /etc/systemd/system/pagecount.service

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


	8. sudo systemctl enable pagecount
	   sudo systemctl start pagecount

	9. sudo nano /etc/rc.local

startx /usr/bin/chromium-browser --kiosk 0.0.0.0:8000 --incognito --window-size=1920,1080 --no-sandbox --noerrdialogs

python /home/pi/off_switch.py

#TESTING
gunicorn --worker-class gevent --timeout 90  --bind 0.0.0.0:8000 wsgi --workers 2
