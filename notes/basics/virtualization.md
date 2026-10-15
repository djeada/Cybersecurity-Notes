# Virtualization

**Virtualization:** The creation of virtual machines (VMs) housed within an operating system (OS).

### Virtual Machines (VMs) and Virtual Desktop Environment (VDE)

**Pros:**
- **Flexible and Portable:** Easy to move and manage across different environments.
- **Safe Testing:** Allows for the controlled testing of malware in isolated environments.

**Cons:**
- **Resource Intensive:** Requires significant CPU, memory, and storage resources.
- **Vulnerable to Hardware Failures:** All virtual machines on a host are affected if the host hardware fails.

---

### VM Categories

1. **System Virtual Machine:**
   - **Description:** Runs an entire OS as a virtual machine.
   
2. **Process Virtual Machine:**
   - **Description:** Runs a single application (e.g., a web browser) within a virtualized environment.

**Related Concepts:**
- **Virtualization vs. Emulation vs. Simulation:** 
  - **Virtualization:** Running multiple OS environments on a single physical machine.
  - **Emulation:** Mimicking one system on another, typically for compatibility.
  - **Simulation:** Imitating the behavior of a system, often for testing and analysis.

- **Virtual Appliance vs. Image vs. Virtual Machine:**
  - **Virtual Appliance:** Pre-configured virtual machine images designed for specific tasks.
  - **Image:** A snapshot or clone of a virtual machine's disk state.
  - **Virtual Machine:** A complete OS environment running in a virtualized state.

**Other Forms of Virtualization:**
- **VPN (Virtual Private Network):** Extends a private network across a public network.
- **VDI (Virtual Desktop Infrastructure):** Delivers desktop environments as a managed service.
- **VLAN (Virtual Local Area Network):** Segments network traffic logically within a single physical network.

---

### Hypervisor (Virtual Machine Manager)

**Description:** Allows multiple virtual OS instances to run concurrently on a single physical machine.

**Type 1 vs. Type 2 Hypervisor:**

- **Type 1 - Native:**
  - **Runs Directly on Host Hardware:** More efficient and flexible but has strict hardware and software requirements.
  - **Use Case:** Common in enterprise environments where performance is critical.

- **Type 2 - Hosted:**
  - **Runs on a Host OS:** Less efficient due to the additional OS layer, but more accessible for general users.
  - **Use Case:** Suitable for development and testing environments on consumer-grade hardware.

---

### Application Containerization

**Description:** Runs distributed applications without the need for a full virtual machine, leading to better efficiency but at the cost of reduced security.

---

### Securing Virtual Machines

**General Considerations:** Securing VMs involves similar strategies to securing physical machines but with additional layers of management.

**Steps to Secure VMs:**
1. **Update Virtual Machine Software:** Keep virtualization software (e.g., VirtualBox, VMware) up to date.
2. **Monitor VM-VM and VM-Host Network Connections:** Be cautious of potential security risks in inter-VM communication.
3. **Protect NAS and SAN:** Ensure that network-attached storage (NAS) and storage area networks (SAN) are secured from virtual hosts.
4. **Disable Unnecessary Ports:** Limit the use of USB and other external ports on virtual machines to prevent unauthorized access.
5. **Alter Boot Priority:** Adjust the virtual BIOS settings to control boot order and enhance security.
6. **Limit and Monitor Resource Usage:** Prevent denial of service (DoS) attacks by monitoring and limiting VM resource allocation.
7. **Protect VM Images:** Secure raw virtual machine images through snapshots, encryption, access permissions, and digital signatures.

---

### Virtualization Sprawl

**Description:** Occurs when there are too many virtual machines to manage effectively, leading to potential security and management issues.

**Solution:**
- **VMLM (Virtual Machine Lifecycle Management) Tool:** Use specialized tools to manage the lifecycle of virtual machines efficiently, including creation, monitoring, and decommissioning.
