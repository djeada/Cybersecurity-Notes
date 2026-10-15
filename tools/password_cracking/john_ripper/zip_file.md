# John the Ripper: ZIP Files

Cracking a Password Protected Zip File

Yes! You read that right. We can use John to crack the password on password protected Zip files. Again, we're going to be using a separate part of the john suite of tools to convert the zip file into a format that John will understand, but for all intents and purposes, we're going to be using the syntax that you're already pretty familiar with by now.


Zip2John

Similarly to the unshadow tool that we used previously, we're going to be using the zip2john tool to convert the zip file into a hash format that John is able to understand, and hopefully crack. The basic usage is like this:

zip2john [options] [zip file] > [output file]

[options] - Allows you to pass specific checksum options to zip2john, this shouldn't often be necessary

[zip file] - The path to the zip file you wish to get the hash of

> - This is the output director, we're using this to send the output from this file to the...

[output file] - This is the file that will store the output from

Example Usage

zip2john zipfile.zip > zip_hash.txt

Cracking

We're then able to take the file we output from zip2john in our example use case called "zip_hash.txt" and, as we did with unshadow, feed it directly into John as we have made the input specifically for it.

john --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt

Practical

Now have a go at cracking the attached "secure" zip file!
