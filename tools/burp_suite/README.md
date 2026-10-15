# Burp Suite

Burp Suite is an intercepting proxy for examining HTTP requests and responses in
authorized web application assessments.

## Basic workflow

1. Start a temporary project and use Burp's browser, or configure a separate lab
   browser with the [FoxyProxy instructions](foxy_proxy.md).
2. Set the target scope to the application you are authorized to test.
3. Leave **Proxy → Intercept → Intercept is off** while browsing normally.
   Traffic passing through the proxy still appears in HTTP history; disabling
   interception does not prevent capture or reduce the traffic sent to Burp.
4. Turn interception on when you need to pause and inspect a particular request.
   Forward or drop it, then switch interception off when finished.
5. Send a selected request to Repeater to change one input and compare responses.
6. Record a reproducible finding, impact, and remediation; avoid retaining secrets
   in exported project files.

Use a dedicated browser profile for testing. If you install Burp's CA certificate
for HTTPS interception, restrict that trust to the lab profile and remove it when
finished. Automated scanning and repeated requests can change application state
or consume resources; agree on scope and limits first.

See [web application security](../../notes/basics/web_application_security.md).

## Sources

- [PortSwigger Burp documentation](https://portswigger.net/burp/documentation)
- [Intercepting HTTP traffic](https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic)
