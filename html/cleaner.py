import time
import os
#Cleans the downloaded files after 10-15mins.
while True:
    one_minute_ago = time.time() - 600
    six_hr=time.time() - 10800
    folder = '$PWD/files'
    os.chdir(folder)
    for somefile in os.listdir('.'):
        if somefile.endswith("_None.mp4"):
            st=os.stat(somefile)
            mtime=st.st_mtime
            if mtime < six_hr:
                print('remove %s'%somefile)
                os.unlink(somefile) # uncomment only if you are sure
        else:
            st=os.stat(somefile)
            mtime=st.st_mtime
            if mtime < one_minute_ago:
                print('remove %s'%somefile)
                os.unlink(somefile) # uncomment only if you are sure
    time.sleep(300)

