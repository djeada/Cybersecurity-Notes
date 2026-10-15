# OWASP Juice Shop

## Let's Go on an Adventure!

This section doesn't require any hacking or technical actions—just follow along.

### Q1. What's the Administrator's Email Address?

#### Action

The reviews show each user's email address. Click on the "Apple Juice" product to find the Administrator's email.

**Ans:** admin@juice-sh.op

**Explanation:**  
By reviewing the product details, specifically the "Apple Juice" product, you can identify the Administrator's email address from the reviews provided.

### Q2. What Parameter is Used for Searching?

#### Action

Click on the magnifying glass in the top right of the application to open the search bar. Enter some text and press "Enter" to search. Pay attention to the URL, which will update with the text you entered. 

The search parameter is visible after the `/#/search?` portion of the URL.

**Ans:** q

**Explanation:**  
The search functionality uses the parameter `q` to pass the search query in the URL, which is a common practice in web applications.

### Q3. What Show Does Jim Reference in His Review?

#### Action

Jim reviewed the "Green Smoothie" product and mentioned a "replicator." A quick Google search for "replicator" indicates that it is from the TV show Star Trek.

**Ans:** Star Trek

## Inject the Juice

**Important:** Ensure that Burp Suite's intercept is on and that your browser is configured to send traffic through Burp Suite.

### Understanding Injection Vulnerabilities

In this section, we will focus on injection vulnerabilities. Follow the steps carefully.

1. Open the attached VM’s IP address in your browser and start Burp Suite.
2. Navigate to the "Account / Login" page.
3. In Burp Suite, turn on Intercept, and set your browser’s proxy (using FoxyProxy) to route traffic through Burp Suite.
4. Attempt to log in with any credentials to capture the request in Burp.

#### Sample Request:

```json
{"email":"abc@def.com","password":"123and4"}
```

### Q1. Log into the Administrator Account!

#### Action

Modify the captured request to inject a SQL true value (`1=1`). This forces the query to always return true.

Modified Request:

```json
{"email":"abc@def.com' or 1=1--","password":"123and4"}
```

Forward the request through Burp Suite to log in as the Administrator.

**Ans:** 32a5e0f21372bcc1000a6088b93b458e41f0e02a

**Explanation:**  
The `1=1` injection forces the SQL query to evaluate as true, bypassing authentication and allowing access to the Administrator account.

### Q2. Log into the Bender Account!

#### Action

Similar to Q4, but this time use the email `bender@juice-sh.op`. Since we know the valid email address, we don't need to use `1=1`. Instead, simply inject a comment to terminate the rest of the SQL query.

Modified Request:

```json
{"email":"bender@juice-sh.op'--","password":"123and4"}
```

Forward the request to log in as Bender.

**Ans:** fb364762a3c102b2db932069c0e6b78e738d4066

**Explanation:**  
By knowing the exact email, the SQL query naturally returns true, and the double dash (`--`) comments out the rest of the query, successfully logging in as Bender.

## Who Broke My Lock?!

In this task, we investigate some authentication flaws.

### Q1. Bruteforce the Administrator Account’s Password!

#### Action

Weak passwords are easy to brute force. Let’s fire up Burp Suite again and start an attack.

1. Capture the login request using Burp Proxy.
2. Send the login request to the Intruder module by pressing `Ctrl + I` (or right-click and select the option from the menu).
3. Clear the § symbols by clicking the "Clear §" button on the right.
4. Edit the login request, substituting the password value in a Sniper bruteforce attack:

   ```json
   {"email":"admin@juice-sh.op","password":"§§"}
   ```

5. Use the `usr/share/wordlists/SecLists/Passwords/Common-Credentials/best1050.txt` wordlist and start the attack.
6. Look for the 200 status code indicating a successful login. The password for the admin user is `admin123`.

**Ans:** c2110d06dc6f81c67cd8099ff0ba601241f1ac0e

**Explanation:**  
By leveraging Burp Suite's Intruder module, you can automate a brute force attack to crack weak passwords, such as `admin123`, allowing you to log in as the administrator.

### Q2. Reset Jim’s Password!

#### Action

Follow the instructions provided in the task to reset Jim’s password.

**Ans:** 094fbc9b48e525150ba97d05b942bbf114987257

**Explanation:**  
The task guides you through the process of resetting Jim’s password. By carefully following the instructions, you can retrieve the necessary information to reset the password successfully.

## AH, Don’t Look!

This task involves exposing sensitive information to the public.

### Q1. Access the Confidential Document!

#### Action

Check the "About Us" page for a link to the `/ftp/` directory on the server. Open the directory in the browser, download the `acquisitions.md` file, and return to the homepage to find the answer.

**Ans:** edf9281222395a1c5fee9b89e32175f1ccf50c5b

**Explanation:**  
The `ftp/` directory contains sensitive documents that can be accessed publicly. By downloading the `acquisitions.md` file, you can extract the required information.

### Q4. Log into MC SafeSearch’s Account!

#### Action

Follow the provided instructions to find the necessary details to log into MC SafeSearch’s account.

**Ans:** 66bdcffad9e698fd534003fbb3cc7e2b7b55d7f0

**Explanation:**  
The instructions provide a clear path to accessing MC SafeSearch’s account. By following them, you can retrieve the necessary login credentials.

### Q5. Download the Backup File!

#### Action

Follow the instructions to locate the `package.json.bak` file. Initially, you may not be able to download it. Use the Poison NULL Byte character bypass (`%00` encoded as `%2500`) and add the `.md` extension to the filename to successfully download it.

**Ans:** bfc1e6b4a16579e85e06fee4c36ff8c02fb13795

**Explanation:**  
The Poison NULL Byte technique allows bypassing certain restrictions when downloading files. By applying this method, you can successfully download the `package.json.bak` file.

## Who’s Flying This Thing?

### Q1. Access the Administration Page!

#### Action

Follow the instructions provided to locate the admin area. Use the admin credentials previously found to log in. Upon navigating to the admin area, the answer will be revealed.

**Ans:** 946a799363226a24822008503f5d1324536629a0

**Explanation:**  
By accessing the administration page with the correct credentials, you can uncover important information, such as the answer provided.

### Q2. View Another User’s Shopping Basket!

#### Action

Remain logged in as the admin user and open Burp Suite. Intercept the connection when checking the shopping basket (Your Basket).

You’ll see a GET request like this:

```
GET /rest/basket/1 HTTP/1.1
```

Modify the request to target the next user’s account:

```
GET /rest/basket/2 HTTP/1.1
```

**Ans:** 41b997a36cc33fbe4f0ba018474e19ae5ce52121

**Explanation:**  
By altering the GET request in Burp Suite, you can view the shopping baskets of other users, revealing sensitive information.

### Q3. Remove All 5-Star Reviews!

#### Action

This can be accomplished in the admin area by following the task instructions to remove all 5-star reviews.

**Ans:** 50c97bcce0b895e446d61c83a21df371ac2266ef

**Explanation:**  
As an admin, you have the authority to manage reviews, including removing them. This action directly affects the visible reviews on the platform.

## Where Did That Come From?

In this task, we will explore XSS (Cross-Site Scripting) vulnerabilities.

### Q1. Perform a DOM XSS!

#### Action

Following the instructions, create an `<iframe>` HTML element that triggers a JavaScript alert.

**Ans:** 9aaf4bbea5c30d00a1f5bbcfce4db6d4b0efe0bf

**Explanation:**  
DOM-based XSS exploits vulnerabilities in the client-side code, enabling you to execute arbitrary JavaScript, such as an alert, within the user’s browser.

### Q2. Perform a Persistent XSS!

#### Action

Log in as the admin user again. Navigate to Account > Privacy & Security > Last Login IP. Use Burp Suite to intercept the logout process. Follow the instructions to modify the headers. Log back in and view the result.

**Ans:** 149aa8ce13d7a4a8a931472308e269c94dc5f156

**Explanation:**  
Persistent XSS involves injecting malicious scripts that persist within the application, often stored in the database and executed whenever the affected content is viewed.

### Q3. Perform a Reflected XSS!

#### Action

The web application does not sanitize the ID parameter. Follow the instructions to execute a reflected XSS attack by manipulating this parameter.

**Ans:** 23cefee1527bde039295b2616eeb29e1edc660a0

**Explanation:**  
Reflected XSS occurs when user-supplied data is immediately returned by the application without proper validation or escaping, allowing the execution of malicious scripts.

## Exploration!

### Q1. Explore and Return to the Home Page

#### Action

Navigate through the provided URL and explore the site. When you return to the home page, the answer will be displayed.

**Ans:** 7efd3174f9dd5baa03a7882027f2824d2f72d86e

**Explanation:**  
Exploring the site and returning to the home page reveals the answer, which might be related to hidden or dynamically generated content.
