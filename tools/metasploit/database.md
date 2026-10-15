# Metasploit Database

While it is not required when interacting with a single target on TryHackMe, an actual penetration testing engagement will likely have several targets. 


Metasploit has a database function to simplify project management and avoid possible confusion when setting up parameter values. 


You will first need to start the PostgreSQL database, which Metasploit will use with the following command: 

systemctl start postgresql


Then you will need to initialize the Metasploit Database using the msfdb init command. 


Starting Postgresql

           
root@attackbox:~# systemctl start postgresql 
root@attackbox:~# msfdb init
[i] Database already started
[+] Creating database user 'msf'
[+] Creating databases 'msf'
[+] Creating databases 'msf_test'
[+] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[+] Creating initial database schema
/usr/share/metasploit-framework/vendor/bundle/ruby/2.7.0/gems/activerecord-4.2.11.3/lib/active_record/connection_adapters/abstract_adapter.rb:84: warning: deprecated Object#=~ is called on Integer; it always returns nil
root@attackbox:~#


You can now launch msfconsole and check the database status using the db_status command.

Checking the database status

           
msf6 > db_status
[*] Connected to msf. Connection type: postgresql.
msf6 >



The database feature will allow you to create workspaces to isolate different projects. When first launched, you should be in the default workspace. You can list available workspaces using the workspace command. 

Listing workspaces

           
msf6 > workspace
* default
msf6 >


You can add a workspace using the -a parameter or delete a workspace using the -d parameter, respectively. The screenshot below shows that a new workspace named "tryhackme" was created.

Adding a workspace

           
msf6 > workspace -a tryhackme
[*] Added workspace: tryhackme
[*] Workspace: tryhackme
msf5 > workspace
default
* tryhackme
msf6 >


You will also notice that the new database name is printed in red, starting with a * symbol.

You can use the workspace command to navigate between workspaces simply by typing workspace followed by the desired workspace name. 

Changing workspaces

           
msf6 > workspace
default
* tryhackme
msf5 > workspace default
[*] Workspace: default
msf5 > workspace 
tryhackme
* default
msf6 >


You can use the workspace -h command to list available options for the workspace command. 

Workspace help menu

           
msf6 > workspace -h
Usage:
workspace                  List workspaces
workspace -v               List workspaces verbosely
workspace [name]           Switch workspace
workspace -a [name] ...    Add workspace(s)
workspace -d [name] ...    Delete workspace(s)
workspace -D               Delete all workspaces
workspace -r     Rename workspace
workspace -h               Show this help information


Different from regular Metasploit usage, once Metasploit is launched with a database, the help command, you will show the Database Backends Commands menu.

Database backend commands

           
Database Backend Commands
=========================

Command           Description
-------           -----------
analyze           Analyze database information about a specific address or address range
db_connect        Connect to an existing data service
db_disconnect     Disconnect from the current data service
db_export         Export a file containing the contents of the database
db_import         Import a scan result file (filetype will be auto-detected)
db_nmap           Executes nmap and records the output automatically
db_rebuild_cache  Rebuilds the database-stored module cache (deprecated)
db_remove         Remove the saved data service entry
db_save           Save the current data service connection as the default to reconnect on startup
db_status         Show the current data service status
hosts             List all hosts in the database
loot              List all loot in the database
notes             List all notes in the database
services          List all services in the database
vulns             List all vulnerabilities in the database
workspace         Switch between database workspaces


If you run a Nmap scan using the db_nmap shown below, all results will be saved to the database. 

The db_nmap command

           
msf6 > db_nmap -sV -p- 10.10.12.229
[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2021-08-20 03:15 UTC
[*] Nmap: Nmap scan report for ip-10-10-12-229.eu-west-1.compute.internal (10.10.12.229)
[*] Nmap: Host is up (0.00090s latency).
[*] Nmap: Not shown: 65526 closed ports
[*] Nmap: PORT      STATE SERVICE            VERSION
[*] Nmap: 135/tcp   open  msrpc              Microsoft Windows RPC
[*] Nmap: 139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
[*] Nmap: 445/tcp   open  microsoft-ds       Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
[*] Nmap: 3389/tcp  open  ssl/ms-wbt-server?
[*] Nmap: 49152/tcp open  msrpc              Microsoft Windows RPC
[*] Nmap: 49153/tcp open  msrpc              Microsoft Windows RPC
[*] Nmap: 49154/tcp open  msrpc              Microsoft Windows RPC
[*] Nmap: 49158/tcp open  msrpc              Microsoft Windows RPC
[*] Nmap: 49162/tcp open  msrpc              Microsoft Windows RPC
[*] Nmap: MAC Address: 02:CE:59:27:C8:E3 (Unknown)
[*] Nmap: Service Info: Host: JON-PC; OS: Windows; CPE: cpe:/o:microsoft:windows
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 94.91 seconds
msf6 >


You can now reach information relevant to hosts and services running on target systems with the hosts and services commands, respectively. 

Hosts and services

           
msf6 > hosts

Hosts
=====

address       mac                name                                        os_name  os_flavor  os_sp  purpose  info  comments
-------       ---                ----                                        -------  ---------  -----  -------  ----  --------
10.10.12.229  02:ce:59:27:c8:e3  ip-10-10-12-229.eu-west-1.compute.internal  Unknown                    device         

msf6 > services
Services
========

host          port   proto  name               state  info
----          ----   -----  ----               -----  ----
10.10.12.229  135    tcp    msrpc              open   Microsoft Windows RPC
10.10.12.229  139    tcp    netbios-ssn        open   Microsoft Windows netbios-ssn
10.10.12.229  445    tcp    microsoft-ds       open   Microsoft Windows 7 - 10 microsoft-ds workgroup: WORKGROUP
10.10.12.229  3389   tcp    ssl/ms-wbt-server  open   
10.10.12.229  49152  tcp    msrpc              open   Microsoft Windows RPC
10.10.12.229  49153  tcp    msrpc              open   Microsoft Windows RPC
10.10.12.229  49154  tcp    msrpc              open   Microsoft Windows RPC
10.10.12.229  49158  tcp    msrpc              open   Microsoft Windows RPC
10.10.12.229  49162  tcp    msrpc              open   Microsoft Windows RPC

msf6 >


The hosts -h and services -h commands can help you become more familiar with available options. 

Once the host information is stored in the database, you can use the hosts -R command to add this value to the RHOSTS parameter. 


Example Workflow

    We will use the vulnerability scanning module that finds potential MS17-010 vulnerabilities with the use auxiliary/scanner/smb/smb_ms17_010 command.
    We set the RHOSTS value using hosts -R.
    We have typed show options to check if all values were assigned correctly. (In this example, 10.10.138.32 is the IP address we have scanned earlier using the db_nmap command)
    Once all parameters are set, we launch the exploit using the run or exploit command. 

Using saved hosts

           
msf6 > use auxiliary/scanner/smb/smb_ms17_010 
msf5 auxiliary(scanner/smb/smb_ms17_010) > hosts -R 

Hosts
=====

address       mac                name                                        os_name  os_flavor  os_sp  purpose  info  comments
-------       ---                ----                                        -------  ---------  -----  -------  ----  --------
10.10.12.229  02:ce:59:27:c8:e3  ip-10-10-12-229.eu-west-1.compute.internal  Unknown                    device         

RHOSTS => 10.10.12.229

msf6 auxiliary(scanner/smb/smb_ms17_010) > show options 

Module options (auxiliary/scanner/smb/smb_ms17_010):

Name         Current Setting                                                 Required  Description
----         ---------------                                                 --------  -----------
CHECK_ARCH   true                                                            no        Check for architecture on vulnerable hosts
CHECK_DOPU   true                                                            no        Check for DOUBLEPULSAR on vulnerable hosts
CHECK_PIPE   false                                                           no        Check for named pipe on vulnerable hosts
NAMED_PIPES  /usr/share/metasploit-framework/data/wordlists/named_pipes.txt  yes       List of named pipes to check
RHOSTS       10.10.12.229                                                    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:'
RPORT        445                                                             yes       The SMB service port (TCP)
SMBDomain    .                                                               no        The Windows domain to use for authentication
SMBPass                                                                      no        The password for the specified username
SMBUser                                                                      no        The username to authenticate as
THREADS      1                                                               yes       The number of concurrent threads (max one per host)

msf6 auxiliary(scanner/smb/smb_ms17_010) > run


If there is more than one host saved to the database, all IP addresses will be used when the hosts -R command is used. 

In a typical penetration testing engagement, we could have the following scenario: 

    Finding available hosts using the db_nmap command
    Scanning these for further vulnerabilities or open ports (using a port scanning module) 


The services command used with the -S parameter will allow you to search for specific services in the environment.

Querying the database for services

           
msf6 > services -S netbios                                                                                       
Services                                                                                                             
========                                                                                                             
                                                                                                                
host          port  proto  name         state  info                                                                              
----          ----  -----  ----         -----  ----                                                                              
10.10.12.229  139   tcp    netbios-ssn  open   Microsoft Windows netbios-ssn

msf6 >


You may want to look for low-hanging fruits such as:

    HTTP: Could potentially host a web application where you can find vulnerabilities like SQL injection or Remote Code Execution (RCE). 
    FTP: Could allow anonymous login and provide access to interesting files. 
    SMB: Could be vulnerable to SMB exploits like MS17-010
    SSH: Could have default or easy to guess credentials
    RDP: Could be vulnerable to Bluekeep or allow desktop access if weak credentials were used. 


As you can see, Metasploit has many features to aid in engagements such as the ability to compartmentalize your engagements into workspaces, analyze your results at a high level, and quickly import and explore data.
