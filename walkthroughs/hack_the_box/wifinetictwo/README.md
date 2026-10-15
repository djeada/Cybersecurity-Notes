# WifineticTwo

- **Start of nmap:**
  The initial step involves conducting an nmap scan, a powerful network scanning tool used to discover hosts and services on a computer network. This scan is essential for identifying open ports and the services running on them, providing a comprehensive view of the target's network. By knowing which ports are open and which services are active, you can tailor your attack strategy to exploit known vulnerabilities in those services.

- **Discovering OpenPLC, looking for default credentials and logging in with openplc:openplc:**
  After identifying the presence of an OpenPLC (Programmable Logic Controller) service through the nmap scan, the next step is to attempt to log in using default credentials. OpenPLC is a common control system, and often, administrators neglect to change the default login credentials (openplc:openplc), which can be exploited to gain unauthorized access. Logging in with these credentials allows initial access to the system, potentially exposing control over critical infrastructure components.

- **Uploading a C reverse shell to OpenPLC:**
  Once logged into the OpenPLC, the next step is to upload a reverse shell written in C. A reverse shell is a type of payload that, when executed, connects back to the attacker's machine, providing remote control over the target system. This step is crucial as it establishes a persistent foothold within the target environment, allowing for further exploitation and control over the compromised system.

- **Talking about our shell hanging our webserver, showing a POC that runs system() to background a process which seems to be smart:**
  After gaining a shell, it was observed that the reverse shell payload caused performance issues with the webserver, likely due to resource contention. To address this, a proof of concept (POC) is demonstrated that uses the system() function to run processes in the background. This technique ensures that the reverse shell remains active without disrupting the webserver's operations, illustrating a clever workaround to maintain stability while retaining control.

- **Discovering a Wireless NIC, running IW to see wireless networks and OneShot to attack WPS:**
  Further exploration reveals a Wireless Network Interface Card (NIC) on the target machine. Using the `iw` tool, a command-line utility for managing wireless devices, the attacker lists available wireless networks. The next step involves using `OneShot`, a tool designed to exploit vulnerabilities in Wi-Fi Protected Setup (WPS), to attack the wireless network. This aims to gain unauthorized access to the wireless network, potentially exposing additional attack vectors and sensitive data.

- **Joining the Wireless Network, showing how important it is to tell DHCLIENT to not update default routes:**
  After successfully attacking the wireless network, the next step is to join it. It's crucial to configure the DHCP client (DHCLIENT) to avoid updating the default network routes automatically. If DHCLIENT updates the routes, it might disrupt the established network connections, including the reverse shell. By preventing route updates, the attacker ensures continuous connectivity and stability of the compromised environment.

- **Cheating to get a root shell, so we can show the routing table of the container that can no longer talk to us:**
  To further explore the network configurations and potential issues, the attacker obtains a root shell using unspecified methods ("cheating"). With root access, the routing table of a container that has lost connectivity is displayed. This step helps in diagnosing network misconfigurations or issues that might have caused the connectivity loss, providing insights for further exploitation or remediation.

- **Adding unset new_routers to a DHCLIENT Enter Hook so it doesn't update routes:**
  To ensure that network routes remain unchanged upon future DHCP renewals, the attacker modifies the DHCP client configuration. By adding the command `unset new_routers` to a DHCLIENT Enter Hook, the DHCP client is instructed not to update the default routes. This ensures that the network configuration remains stable, preventing disruptions in connectivity that could interfere with the ongoing exploitation.

- **Once we get on the Wireless Network we can SSH to OpenWRT and get the root flag:**
  After successfully connecting to the wireless network, the attacker uses SSH (Secure Shell) to access an OpenWRT device. OpenWRT is a widely used open-source firmware for routers. By gaining SSH access, the attacker retrieves the root flag, a key objective often used in Capture The Flag (CTF) exercises to indicate successful exploitation.

- **Showing we could exploit OpenWRT through the web interface as well, setting up a pivot with Chisel:**
  An alternative exploitation method is demonstrated by targeting the OpenWRT device's web interface. Chisel, a fast TCP/UDP tunnel that can be used to bypass firewalls, is set up to create a pivot. This allows the attacker to route traffic through the compromised OpenWRT device, enabling further exploitation of systems behind the firewall or in other network segments.

- **Logging into OpenWRT with a blank password, going to the Scheduled Tasks to create a cron:**
  The attacker logs into the OpenWRT device using a blank password, highlighting poor security practices. Once logged in, they navigate to the Scheduled Tasks section to create a cron job. A cron job is a scheduled task that can run at specified intervals, often used to maintain persistence by ensuring that malicious payloads are re-executed periodically.

- **Creating a Reverse Shell Payload with MSFVenom:**
  Using MSFVenom, a tool from the Metasploit framework, the attacker generates a reverse shell payload. MSFVenom is highly versatile, capable of creating payloads in various formats for different platforms. The generated reverse shell is designed to connect back to the attacker's machine, providing remote access to the compromised system.

- **Getting multiple reverse shells so we can easily run multiple commands on the container:**
  To facilitate easier command execution and control over the compromised container, multiple reverse shells are established. This allows the attacker to run several commands simultaneously, enhancing their ability to perform various actions such as data exfiltration, further exploitation, and maintaining control over the system.
