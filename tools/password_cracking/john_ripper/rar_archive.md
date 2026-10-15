# John the Ripper: RAR Archives

Cracking a Password Protected RAR Archive

We can use a similar process to the one we used in the last task to obtain the password for rar archives. If you aren't familiar, rar archives are compressed files created by the Winrar archive manager. Just like zip files they compress a wide variety of folders and files.

Rar2John

Almost identical to the zip2john tool that we just used, we're going to use the rar2john tool to convert the rar file into a hash format that John is able to understand. The basic syntax is as follows:

rar2john [rar file] > [output file]

rar2john - Invokes the rar2john tool

[rar file] - The path to the rar file you wish to get the hash of

> - This is the output director, we're using this to send the output from this file to the...
[output file] - This is the file that will store the output from

Example Usage

rar2john rarfile.rar > rar_hash.txt


Cracking

Once again, we're then able to take the file we output from rar2john in our example use case called "rar_hash.txt" and, as we did with zip2john we can feed it directly into John..

john --wordlist=/usr/share/wordlists/rockyou.txt rar_hash.txt
