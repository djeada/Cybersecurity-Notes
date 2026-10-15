# Burp Suite

Here's a step-by-step guide on how to configure the FoxyProxy addon for your browser:

### Step 1: Install FoxyProxy Addon
1. **For Firefox:**
   - Go to the [FoxyProxy Standard addon page](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/).
   - Click on the "Add to Firefox" button.
   - Confirm any prompts to install the addon.

2. **For Google Chrome:**
   - Go to the [FoxyProxy Standard extension page](https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp).
   - Click on the "Add to Chrome" button.
   - Confirm the installation by clicking "Add extension" in the prompt.

### Step 2: Open FoxyProxy Settings
1. After installing, you'll see the FoxyProxy icon in your browser's toolbar.
   - **Firefox:** It looks like a blue or orange fox wrapped around a globe.
   - **Chrome:** It looks like a globe with a small blue fox.

2. Click on the FoxyProxy icon and select "Options" or "Settings" from the dropdown menu. This will open the FoxyProxy configuration page.

### Step 3: Add a New Proxy
1. In the FoxyProxy settings, click on "Add" or "Add New Proxy" to configure a new proxy server.

2. A form will appear where you can input the proxy details:
   - **Title:** Give the proxy a name, like "My Proxy." or "BURP"
   - **Proxy Type:** Select the type of proxy you’re using (HTTP, HTTPS, SOCKS5, etc.), usually will be just HTTP.
   - **Proxy IP Address or DNS Name:** Enter the IP address or domain name of the proxy server (for local setup it's 127.0.0.1).
   - **Port:** Enter the port number your proxy server uses (e.g., 8080, 3128, 1080)  default for any proxy is 8080.
   - **Username and Password:** If your proxy requires authentication, enter the credentials here.
   - **Select Color:** (Optional) You can assign a color to this proxy setting for easier identification.
  
3. Click "Save" to store the new proxy configuration.

### Step 4: Configure FoxyProxy to Use the Proxy
1. Go back to the main FoxyProxy settings page.

2. You'll see a list of your configured proxies. Next to each one, there's an "On" and "Off" switch. 

3. Select the proxy you want to use by clicking "On."

### Step 5: Set FoxyProxy Mode
FoxyProxy allows you to control when the proxy is used. You can choose from the following modes:
   - **Disable FoxyProxy:** Turns off all proxy usage.
   - **Use Enabled Proxies by Patterns and Priorities:** This mode uses proxy servers based on URL patterns you define.
   - **Use Enabled Proxies (Global Proxy):** All traffic will go through the selected proxy.
   - **Completely Disable FoxyProxy:** Disables all proxy configurations (useful for direct connections).

To set this, click on the FoxyProxy icon and choose the desired mode from the dropdown menu.

### Step 6: Testing the Proxy
1. After configuring FoxyProxy, visit a website like [WhatIsMyIP](https://www.whatismyip.com/) to verify that your IP address matches the IP of the proxy server you configured.

2. If the proxy is working correctly, you should see the proxy server's IP address instead of your real IP.

### Additional Tips:
- **URL Patterns:** You can configure FoxyProxy to only use the proxy for specific URLs or domains by setting up patterns. This is useful if you only want to route certain traffic through the proxy.
- **Multiple Proxies:** If you have multiple proxy configurations, you can easily switch between them using the FoxyProxy icon in your toolbar.
