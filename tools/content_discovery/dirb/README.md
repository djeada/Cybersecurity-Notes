# Dirb

The image you provided shows a command that is being used in a terminal or command-line interface. The command is:

```bash
dirb http://10.0.2.9
```

### Explanation:

- **`dirb`**: This is a web content scanner command, which is commonly used in cybersecurity and penetration testing to discover hidden web content, such as directories and files on a web server. It works by performing a brute-force attack using a wordlist to try to locate directories and files that are not linked or visible from the main web page.

- **`http://10.0.2.9`**: This is the target web server or IP address that the `dirb` tool is scanning. In this case, `10.0.2.9` is an IP address, likely within a private network, which suggests that the command is being run in a controlled environment, such as during a penetration testing exercise or a CTF (Capture the Flag) challenge.

When you run this command, `dirb` will attempt to find directories and files on the web server located at `http://10.0.2.9` by using a predefined wordlist. The results can help in identifying hidden resources on the server that might be accessible without proper authorization.

This tool is often used to identify potential attack vectors in a web application, such as unprotected admin panels, configuration files, or backup files.


DISABLE RECURSIVE TO INDETIFY QUICKLY THE DIRECTORIES: -r

flag -R to ask per each dir if we want to go recursive there


To use a custom wordlist with `dirb` and save the results to a file, you can use the following command structure:

### Using a Custom Wordlist

To use a custom wordlist, you can specify the path to your wordlist using the `-w` option.

### Saving Results to a File

To save the results to a file, you can use the `-o` option followed by the desired output file path.

### Example Command:

```bash
dirb http://10.0.2.9 /path/to/custom_wordlist.txt -o /path/to/save_results.txt
```

### Breakdown:

- **`http://10.0.2.9`**: The target URL or IP address you want to scan.
- **`/path/to/custom_wordlist.txt`**: The path to your custom wordlist file.
- **`-o /path/to/save_results.txt`**: The `-o` option tells `dirb` to save the output to the specified file. Replace `/path/to/save_results.txt` with the actual path where you want to save the results.

### Example with Actual Paths:

```bash
dirb http://10.0.2.9 /usr/share/wordlists/my_custom_wordlist.txt -o /home/user/dirb_results.txt
```

In this example:
- The custom wordlist is located at `/usr/share/wordlists/my_custom_wordlist.txt`.
- The results will be saved to `/home/user/dirb_results.txt`.


The `-X` option in `dirb` is used to specify file extensions that `dirb` should append to each word in the wordlist when performing the scan. This option is useful when you want to search for specific types of files on the target server.

### How It Works:

When you provide one or more file extensions using the `-X` option, `dirb` will take each word from the wordlist and attempt to access it with the specified extensions appended. For example, if you are searching for PHP files, HTML files, or other specific file types, you can use this option to refine your search.

### Example Command:

```bash
dirb http://10.0.2.9 /path/to/wordlist.txt -X .php,.html,.txt
```

### Breakdown:

- **`-X .php,.html,.txt`**: Specifies the file extensions `.php`, `.html`, and `.txt`. 
- **How it works**: 
  - If the wordlist contains the word `admin`, `dirb` will attempt to access `admin.php`, `admin.html`, and `admin.txt` on the target server.
  - Similarly, if the wordlist contains the word `login`, `dirb` will try `login.php`, `login.html`, and `login.txt`.

### Practical Use Case:

Let’s say you are trying to discover different types of files related to a web application, such as PHP scripts, HTML files, and plain text files. Instead of creating multiple wordlists for each file type or running `dirb` multiple times, you can use the `-X` option to append all relevant extensions in one scan.

### Example Output:

If `dirb` finds `login.php` on the server, it will return that as a result. If it doesn’t find `login.html` or `login.txt`, those will not appear in the results.

This option helps in narrowing down the results to specific types of files, making the scanning process more efficient and targeted.

### How It Works:

When you use `-N` followed by an HTTP status code, `dirb` will filter out any responses that match that code. This is useful if you want to ignore specific types of responses, such as `404 Not Found` errors, which are common when scanning for non-existent files or directories.

### Example Command:

```bash
dirb http://10.0.2.9 /path/to/wordlist.txt -N 404
```

### Breakdown:

- **`-N 404`**: This command tells `dirb` to ignore any responses that return a `404 Not Found` status code.
  - **404 Not Found**: This status code indicates that the requested resource could not be found on the server.

### Practical Use Case:

Let's say you are scanning a website and are only interested in finding resources that actually exist or have restricted access. By using `-N 404`, you can filter out all the "Not Found" errors, which are typically less useful during a scan, allowing you to focus on more significant findings like `200 OK` or `403 Forbidden`.

### Example Output:

With `-N 404` specified, `dirb` will not display any results for URLs that result in a `404 Not Found` status. If the server returns `200 OK`, `403 Forbidden`, or any other status code, those will still be shown in the output.
