from os import system
from time import sleep

system("sudo rm -rf times.log")
sleep(1)
count = input("Input the wifi enable/disable count you want: ")

for i in range(int(count)):
    system("echo Times: " + str(i+1) + " >> times.log") 
    print("Times:", i+1)
    system("adb shell svc wifi disable")
    print("Wi-Fi disable")
    sleep(1)
    system("adb shell svc wifi enable")
    print("Wi-Fi enable")
    sleep(5)
    system("adb shell \"ip a | grep wlan0 | grep inet\"")
    sleep(1)
    system("adb shell \"ping -c 1 8.8.8.8\"")
    sleep(1)

print("END")
