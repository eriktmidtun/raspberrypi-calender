#!/bin/sh
#launcher.sh

cd /
cd home/pi/Pi-Calender
sudo modprobe uinput
sudo python buttons.py
cd /
