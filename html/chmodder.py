import time
import os
while True:
    folder = '/home/ubuntu/website/files'
    os.chdir(folder)
    for somefile in os.listdir('.'):
        os.system("sudo chmod 777 {}".format(somefile))
        os.system("sudo chown ubuntu:users {}".format(somefile))
    time.sleep(15)

