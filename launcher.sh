#!/bin/sh
#launcher.sh

cd /
cd home/pi/Pi-Calender
sudo modprobe uinput
sudo python sensor.py &
sudo python buttons.py &
cd /
