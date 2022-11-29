#Use libimobiledevice's idevicebackup2 utility

import subprocess

#Scan for any iDevice
def scan():
        
    #Assume libimobiledevice is installed
    lib_installed = True

    try:
        checkfordevice = subprocess.Popen(["idevicename"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = checkfordevice.communicate()

        #stdout
        if len(output[0].decode()) == 0: #Nothing in stdout = error
            print(output[1].decode())#print error
            return lib_installed, False
        else: 
            print(output[0].decode())#print success
            return lib_installed, True 
    except:
        lib_installed = False

        print("[Error] Looks like libimobiledevice or libimobiledevice-utils is not installed")

        return lib_installed, False   


#Perform backup, restore and cancel actions
class Action:

    process = None

    def backup(self, folder):

        self.process = subprocess.Popen(["idevicebackup2", "backup", folder])

        while(self.process.poll() == None):
            pass

    def restore(self, folder):
        
        self.process = subprocess.Popen(["idevicebackup2", "restore", folder])

        while(self.process.poll() == None):
            pass


    def cancel(self):
        
        self.process.terminate()
        print("Process terminated!")