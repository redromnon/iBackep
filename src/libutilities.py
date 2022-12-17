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

    def backup(self, folder, password):

        #Enable encryption if password is given
        if password is None:
            
            self.process = subprocess.Popen(["idevicebackup2", "backup", folder], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

            return self.process

        else:
            
            print("Checking encryption...")
            self.encrypt_process = subprocess.Popen(["idevicebackup2", "encryption", "on", password, folder])
            self.encrypt_process.wait()

            self.process = subprocess.Popen(["idevicebackup2", "backup", folder], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

            return self.process

    def restore(self, folder, password):
        
        if password is None:
            
            self.process = subprocess.Popen(["idevicebackup2", "restore", folder], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

            return self.process

        else:

            print("Restoring encrypted backup...")
            self.process = subprocess.Popen(["idevicebackup2", "restore", "--password", password, folder], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

            return self.process

    def cancel(self):
        
        self.process.terminate()
        print("Process terminated!")