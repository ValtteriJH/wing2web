# 60 s window for user to activate a separate wlan for the raspberry to connect to

sudo killall wpa_supplicant
sleep 60;sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf &
sudo dhclient wlan0
