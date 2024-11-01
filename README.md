![logo](https://github.com/user-attachments/assets/cc99d06b-9768-4934-be17-6ccac05b8801)

# LipaDNS

LipaDNS is a dynamic DNS (DDNS) management tool designed to monitor and update DNS records automatically whenever an external IP address changes. Built with Python and utilizing Cloudflare's DNS API, LipaDNS is ideal for maintaining up-to-date DNS configurations in environments with frequently changing IP addresses. 

The addition of new nameservers is a core feature that is currently in progress.

## Quick Reference

The following environment variables should be set:
- **REFRESH_RATE**: Sets the time interval (in seconds) at which LipaDNS will check for changes in the external IP address.
- **DOMAIN_NAME**: Specifies the fully qualified domain name (FQDN) that LipaDNS will update. This is the DNS record that LipaDNS will manage, ensuring it always points to the latest external IP.
- **CLOUDFLARE_API_TOKEN**: The API token for authenticating with Cloudflare's API. This token should have sufficient permissions (usually "Edit DNS") to update DNS records within the specified zone.
- **CLOUDFLARE_ZONE_ID**: Identifies the DNS zone in Cloudflare where the DNS record (DOMAIN_NAME) is located.

## Key Features
- **Automatic DNS Updates**: Monitors IP changes and updates DNS records in real time, ensuring domain accuracy and availability.
- **Nameserver Flexibility**: Currently compatible with Cloudflare’s DNS API, with planned support for additional nameservers to provide broader compatibility.
- **Modular Architecture**: Allows easy addition of new DNS providers, simplifying future integrations.
- **Comprehensive Logging & Error Handling**: Ensures high reliability with detailed logging and error management.
- **Environment Configurations**: Uses environment variables for API keys, domain names, and other settings to streamline setup.

## Use Cases
LipaDNS is ideal for applications in dynamic IP environments—like home labs, small businesses, and self-hosted applications—where DNS records need frequent updates. Future compatibility with multiple nameservers also makes LipaDNS a versatile solution for developers and IT professionals seeking a robust and adaptable DDNS management tool.