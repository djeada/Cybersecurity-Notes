# Redundancy Planning

**Redundancy** is essential to prevent single points of failure and ensure the continuous operation of systems.

### Redundant Power

**Objective:** Keep servers and networks operational during power failures, maintaining accessibility and minimizing damage.

**Common Electrical Problems:**
1. **Power Surges & Spikes:** Sudden increases in voltage.
2. **Sags, Brownouts, and Blackouts:** Drops or losses in power supply.
3. **Power Supply Failure:** Total failure of the power supply unit.

**Redundant Power Supplies:**
- **Description:** Enclosures containing two or more power supplies to ensure continuous operation.
- **Common Vendors:** HP, Cisco, Thermaltake, Enlight.

**UPS (Uninterruptible Power Supplies):**
- **Function:** Combines a surge protector with a backup battery to provide temporary power (5-30 minutes) during outages.
- **Features:** Cleans up dirty or noisy power, similar to line conditioners.
- **Comparison:** 
  - **SPS (Standby Power Supply):** Activates during power loss.
  - **UPS (Uninterruptible Power Supply):** Provides instant backup power without interruption.

**Backup Generators:**
- **Purpose:** Serve as an emergency power supply for the entire system.
- **Types:**
  - **Portable Gas Engine**
  - **Permanently Installed**
  - **Battery Inverter**
- **Considerations:**
  1. **Price**
  2. **Manual vs. Automatic Operation**
  3. **Uptime / Capacity, Power Output**
  4. **Fuel Source**
- **Common Vendors:** Generac, Gillette, Kohler.

---

### Redundant Data

**RAID Arrays:**
- **RAID 0:** Data Striping (No redundancy).
- **RAID 1:** Data Mirroring.
- **RAID 5:** Striping with parity.
- **RAID 6:** Striping with double parity.
- **RAID 10:** 2 RAID 1 mirrors striped.

**RAID Classification:**
- **Failure Resistant**
- **Failure Tolerant**
- **Disaster Tolerant**

*Note: Protection scope increases from a to c.*

---

### Redundant Networking

**Server Network Adapters:**
- **Plan:** Install multiple redundant adapters for failover and load balancing.
- **Management:** Consider centralized network adapter management software.

**Main Switch/Router Connection:**
- **Plan:** Always have spare switches/routers to avoid downtime.
- **Topology:** Avoid pure star topologies to reduce single points of failure.

**Internet Connection:**
- **Plan:** Use dual and redundant ISP connections.
- **Consideration:** Implement mirror sites for web content.

---

### Redundant Servers

**Goal:** Minimize server downtime during failures and maximize throughput.

**Failover Clusters:**
- **Purpose:** Secondary server takes over when the primary server fails, ensuring high availability.

**Load Balancing Clusters:**
- **Purpose:** Several servers share resources like CPU, RAM, and hard disk space.
- **Use Case:** Commonly used in DNS, IRC, and FTP servers.
- **Feature:** Can also include failover by replicating data between servers.

---

### Redundant Sites (Physical Locations)

1. **Hot Site:** Complete replication of the entire network, including servers and phone lines.
2. **Warm Site:** Partial replication with some data recovery capabilities.
3. **Cold Site:** Minimal equipment replication; requires setup after disaster.

---

### Redundant People

**Strategy:** Implement role takeover protocols and designate primary and secondary personnel to ensure operations continue during personnel shortages.

---

## Disaster Recovery Plans and Procedures

### Data Backup

**Tape Backup:**
1. **Full Backup:** Complete backup of all data.
2. **Incremental Backup:** Backs up only data that has changed since the last backup.
3. **Differential Backup:** Backs up data that has changed since the last full backup.

**Backup Schemes:**
1. **10 Tape Rotation**
2. **Grandfather-Father-Son Scheme:** Daily, weekly, monthly backups.
3. **Tower of Hanoi Scheme**

**Snapshot Backups:** Capture the state of the system at a specific point in time.

---

### Disaster Recovery (DR) Planning

**Types of Disasters:**
1. **Fire**
2. **Flood**
3. **Long-term Power Loss**
4. **Theft and Attack**
5. **Loss of Building Access**

**Disaster Recovery Plans:**
- **Purpose:** Provide a framework for responding to various disasters with minimal downtime.
- **Contents:**
  - **Contact Info:** Key personnel and service providers.
  - **Impact Evaluation:** Assess asset loss and replacement costs.
  - **Recovery Plan:** Steps to restore operations.
  - **Business Continuity Plan:** Ensure critical operations continue.
  - **Copies of Agreements:** Insurance, service contracts, etc.
  - **Disaster Recovery Drills:** Regularly test and update plans.
  - **Critical Systems and Data List:** Prioritize systems and data for recovery.

## Recovery objectives and backup verification

- **Recovery Point Objective (RPO):** Target maximum amount of data loss expressed
  as time. An RPO of one hour calls for recoverable data no more than one hour old.
- **Recovery Time Objective (RTO):** Target time to restore an agreed service level
  after disruption. A short RTO requires practiced recovery and dependencies.
- **RAID is not a backup:** It can improve availability during disk failure but
  does not independently protect against deletion, ransomware, or site loss.
- Maintain multiple backup copies on separate failure domains, including an
  offline or immutable copy with separately protected administrative access.
- Test restoration, application consistency, encryption-key availability, and the
  actual recovery time. A successful backup job is not proof of recoverability.
- Define recovery order for identity, networking, keys, databases, and applications.
  Restore trusted systems and investigate compromise before reconnecting them.

See [incident response](incident_response.md) and [digital forensics](digital_forensics.md).

## Sources

- [NIST SP 800-34 Rev. 1: Contingency Planning](https://csrc.nist.gov/pubs/sp/800/34/r1/final)
- [CISA StopRansomware Guide](https://www.cisa.gov/stopransomware/ransomware-guide)
