# Installation instructions
* Download Raspberry Pi OS-lite
* Rpi-imager options:
	* set hostname to "u-robot"
	* enable SSH with a public key from your ~/.ssh/*.pub files
*  ```sudo apt update```
*  ```sudo apt upgrade```
* Test pinging : ```ping u-robot.local```
* Test ssh : ```ssh pi@u-robot.local```
*  ```speaker-test -t sine -f 440 -c 2 -s 1```
* Nautilus : [SFTP-folder](sftp://pi@u-robot.local/home/pi)
