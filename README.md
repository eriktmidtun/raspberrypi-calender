# Pi-Calender v1.1
This is an overview of how i made my Raspberry pi controlled calender Kiosk. I have altered some of the files for privacy reasons, this is a public copy of my private repo that is live on the RPi.
UPDATE; Im currently rewriting the whole thing as a react app, with yr.no api, google photos api, and ATB buss api. It is in a seperate private repository. Planning to be done within the year.

## Final look

![Raspberry Pi](/info-files/final/front.jpg "Front")

Back             |  Front
:-------------------------:|:-------------------------:
![Raspberry Pi](/info-files/final/side.jpg "Side with buttons")  |  ![Raspberry Pi](/info-files/final/sensor.jpg "Front with sensor")
![Raspberry Pi](/info-files/final/back.jpg "Back with wiring") | ![Raspberry Pi](/info-files/final/calender.jpg "the calender")


## Hardware
The hardware i used to make it:
* Raspberry Pi Model 3 B+
* 32GB SD card for the Pi, used one I had.
* LCD screen from an old notebook i had, I also used the power adapter from the notebook.
* LCD screen controller board, i used [THIS](https://www.ebay.com/itm/HDMI-DVI-VGA-AUDIO-LCD-Controller-Board-for-N173HGE-L21-1920-1080-DIY-PC-Monitor/360796326496?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m1438.l2649) from Ebay for my perticular screen.
* Momentary Push button switches, i used [THESE](https://www.ebay.com/itm/5pcs-Waterproof-Push-Button-Momentary-Horn-Switch-Start-Metal-16mm-max-250V-3A-/232259034032?hash=item3613b79bb0) from Ebay
* Jumper wires M/F, i used [THESE](https://www.ebay.com/itm/40pc-Breadboard-Dupont-Jump-Wire-M-M-M-F-F-F-10-20-30cm-Jumper-Cable-Lead-2-54mm-/202127939692?var=&hash=item0) from Ebay
* 30cm HDMI cable.

#### How it was connected
Update; some of the wiring is outdated since i added the motion sensor.
I used the GPIO Board mode to find the right pins on the Pi to use.
![Raspberry Pi pins meaning](/info-files/pi-board-layout.png "Pi pins meaning")
I connected three buttons with jumper wires to the Pi pins. The buttons was wired like this:

|  Pin  | Ground     | Button  |
|:-----:|:----------:|:-------:|
| 3     | 6          | prev    |
| 11    | 9          | refresh |
| 1     | 4          | next    |

Diagram of this:
![Wiring diagram](/info-files/buttons-wiring.png "wiring")
Here the black wires are to ground. They could all be connected and go to one single ground pin.

I had one aditional button wich I used for turning the screen on and of with. This one was connected to pins on the LCD controller board. The pins i used for my controller board were(from the left) pin 1 and 4(ground).

The controller board and the Pi is connected with an HDMI cable.

## Setting up the Pi
To use the Pi for anything I had to install an operating system. I went with the default linux-based Raspbian. It can be done on the Raspberry Pi's website. [Install Raspbian](https://www.raspberrypi.org/documentation/installation/installing-images/)

#### Set up SSH Remote control
To make things easier i installed [Putty SSH client](https://www.putty.org) on my windows Laptop, and enabled SSH in the Rasbian settings. I then changed the password for the Pi and got the IP for the Pi with "sudo hostname -I" in Terminal. Then it was easy to connect to the Pi from the laptop in the Putty software with the IP.

#### Small changes
To auto hide the cursor on the Pi, install unclutter with "sudo apt-get install unclutter". Then if you add
'@unclutter -idle 0.1 -root' into /etc/xdg/lxsession/LXDE/autostart
it will start automaticly.

To force the screen to stay on and dont go into sleep mode write 
"sudo nano /etc/ligthdm.conf" 
and add the following line to the [SetDefault] section:
xserver-command= X -s 0dpms

Other changes like rotating screen can be done in "sudo nano /boot/config.txt".
To rotate screen add "display_rotate=3" numbers 1-4.
Disable the overscan(black bars) with "disable_overscan=1"

#### Installing Git and connecting to GitHub
I wanted to setup Git to have full version control and backup of my most important files on the Pi. Installing git can be done with "sudo apt install git-all". Then I made the directory Pi-Calender(mkdir Pi-Calender) and used "git init" to inizialize a repository. I added my GitHub email in "git config --global user.email YOUR-EMAIL" and "git config --global user.name 'FULL NAME'". Then it was only to use SSH with GitHub. I generated a SSH key [THIS WAY](https://help.github.com/articles/working-with-ssh-key-passphrases/#platform-mac) and copied it from "~/.shh/id_rsa.pub" to my GitHub's settings SSH keys. Then I made the Pi-Calender repo on GitHub and copied the SSH link for the repo and wrote "git remote add origin SSH-Link". Git was done setting up.

#### Buttons script and autostart
I made the [buttons.py](/buttons.py "buttons script") based on "How it was connected". I made it to be able to use a button for different actions bassed on how long it was pressed. To use it with virtual keypresses I installed [uinput (download instructions)](http://tjjr.fi/sw/python-uinput/). Uinput full list of [KEYS](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h#L74). To autolaunch it at startup you can do like [THIS](https://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/) and make a [launcher.sh file](/launcher.sh) that does premade command lines and then make it executable with "chmod 755 launcher.sh". Write "sudo crontab -e" and then add @reboot sh /home/pi/Pi-Calender/launcher.sh" to run it at startup. Uploaded buttons.py to Github and used "git pull" to get it to the Pi.

#### Make the calender
I used a local webpage to display the calender. I added a clock and a picture for the top porsion of the webpage, and a google embeded calender which i altered the outdated visuals with [css](/site/calender-skin.cs). To apply the css to the embeded google calender i downloaded a chromium extension that can alter css on webpages. I used [Chrome Stylus extension](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne). Just copy [this css](/site/calender-skin.cs) into the extension with the google embeded url.

The embeded google URL can be found at your google calender settings. Make sure to custimize it with the right height and width and remove the title and such. I use height = 1000px and width = 1080px. The Javascript that autofocuses the calender need the iframe to have an id tag = "calender" .

To make the webpage launch at startup in full size i typed "sudo nano .config/lxsession/LXDE-pi/autostart" in Terminal and added these lines
@chromium-browser --no-startup-window --kiosk
@chromium-browser  --start-maximized --kiosk  file:///home/pi/Pi-Calender/site/calender-site1.html file:///home/pi/Pi-Calender/site/calender-site2.html

I have two webpages that i want to be able to switch between with the buttons, thats why there are two URLs.

UPDATE; I have added a motion sensor for the screen to turn on when it detects movement.
