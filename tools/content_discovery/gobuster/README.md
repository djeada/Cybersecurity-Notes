# Gobuster

 Here's a breakdown of the command:

```bash
gobuster dir -u http://usage.htb -w /opt/SecLists/Discovery/Web-Content/raft-small-words.txt -o root.out
```

### Explanation:
- **gobuster dir**: This is a mode in Gobuster for directory/file brute-forcing. Gobuster can also be used for DNS subdomain enumeration and other tasks, but in this case, it's used to find hidden directories or files on a web server.

- **-u http://usage.htb**: The `-u` flag specifies the URL of the target. In this case, the target is `http://usage.htb`.

- **-w /opt/SecLists/Discovery/Web-Content/raft-small-words.txt**: The `-w` flag specifies the wordlist to use. Here, it's using a wordlist located at `/opt/SecLists/Discovery/Web-Content/raft-small-words.txt`. This file likely contains a list of common directory and file names that Gobuster will try against the target.

- **-o root.out**: The `-o` flag specifies the output file where the results will be saved. Here, the results will be saved to a file named `root.out`.

### What this command does:
This command is using Gobuster to brute-force directories and file names on the web server located at `http://usage.htb`. It uses the wordlist `raft-small-words.txt` to try to find hidden directories or files. The results of this scan will be saved in a file named `root.out`.

This type of command is typically used in penetration testing to discover hidden or unlisted parts of a website that might contain sensitive information or offer a way to exploit the site further.
