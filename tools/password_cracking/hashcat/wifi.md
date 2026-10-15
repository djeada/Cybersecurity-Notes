# Hashcat Setup and Execution Guide

This guide will walk you through the steps to set up a GPU server on Linode, install Hashcat, and run password-cracking tasks using different character sets.

## Step 1: Setup Server in Linode

First, create a GPU instance on Linode. This will provide the necessary hardware acceleration for efficient password cracking with Hashcat.

**Explanation:**  
Linode offers powerful GPU instances ideal for compute-intensive tasks like password cracking. Setting up a server here ensures you have the required resources.

## Step 2: SSH into the Server

Once your server is up and running, connect to it via SSH:

```bash
ssh root@192.168.1.1
```

**Explanation:**  
Replace `192.168.1.1` with the actual IP address of your Linode server. SSH is a secure protocol used to connect to and manage remote servers.

## Step 3: Install Hashcat

Update your server and install Hashcat:

```bash
sudo apt update
sudo apt install hashcat
hashcat -I
```

**Explanation:**  
- `sudo apt update`: Updates the package lists for upgrades and new packages.
- `sudo apt install hashcat`: Installs Hashcat, a powerful password recovery tool.
- `hashcat -I`: Lists the available OpenCL devices, such as GPUs, which Hashcat will use.

## Step 4: Install CUDA

CUDA is required for leveraging the GPU’s power. Follow these steps to install it:

```bash
sudo apt update && sudo apt upgrade
sudo apt install build-essential linux-headers-$(uname -r)
```

**Explanation:**  
- `build-essential` and `linux-headers`: These packages are necessary for building software and kernel modules, which are required for the NVIDIA drivers and CUDA toolkit.

## Step 5: Install NVIDIA Drivers

Download and install the NVIDIA drivers for your GPU:

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
sudo shutdown -r now
```

**Explanation:**  
- The first `wget` command downloads the pin file that helps manage package priorities.
- The second `wget` command downloads the CUDA repository.
- `dpkg` installs the CUDA repository package.
- `sudo apt-get install cuda`: Installs the CUDA toolkit and drivers.
- `shutdown -r now`: Reboots the server to apply changes.

## Step 6: Upload Files to the Server

Use SFTP to transfer the file containing the hashes you want to crack:

```bash
sftp root@192.168.1.1
put 8-digit-wpa2.hc22000
```

**Explanation:**  
SFTP is a secure way to transfer files to and from your server. Replace `192.168.1.1` with your server’s IP address.

## Step 7: Check Available GPUs

Verify that Hashcat recognizes your GPU(s):

```bash
hashcat -I
```

**Explanation:**  
This command lists all the GPUs available for use with Hashcat, ensuring your setup is correctly configured.

## Step 8: Run Hashcat

### 8-Digit Numeric WPA2 Cracking

To crack a WPA2 handshake with an 8-digit numeric password:

```bash
hashcat -m 22000 8-digit-wpa2.hc22000 -a 3 ?d?d?d?d?d?d?d?d -d 6,7,8,9 -w 4
```

**Explanation:**  
- `-m 22000`: Specifies the hash mode for WPA2.
- `-a 3`: Sets the attack mode to brute-force.
- `?d?d?d?d?d?d?d?d`: Defines a mask of 8 digits.
- `-d 6,7,8,9`: Selects specific GPUs.
- `-w 4`: Sets the workload profile to the highest (for maximum GPU usage).

### 10-Character Alphanumeric WPA2 Cracking

To crack a WPA2 handshake with a 10-12 character alphanumeric password:

```bash
hashcat -m 22000 10-digit-letters-wpa.hc22000 --increment --increment-min 10 --increment-max 12 -1 ?d?l?u -a 3 ?1?1?1?1?1?1?1?1?1?1?1?1 -d 6,7,8,9 -w 4
```

**Explanation:**  
- `--increment`: Enables increment mode, starting with the minimum length and increasing.
- `--increment-min 10`: Sets the minimum length of the password to 10 characters.
- `--increment-max 12`: Sets the maximum length to 12 characters.
- `-1 ?d?l?u`: Defines a custom character set including digits, lowercase, and uppercase letters.
- `?1?1?1?1?1?1?1?1?1?1?1?1`: Uses the custom character set for each position in the password.
