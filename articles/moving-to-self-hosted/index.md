+++
title: Self hosting my website with Arch and Certbot
published: 2025-01-27
description: I started self hosting my websites on my own server - part of this was migrating my HTTPS certificates. Here's how I did it.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

I am moving from a hosted solution using Digital Ocean, Certbox and Namecheap to my own server. I will continue with Certbot and Namecheap, but bring my own server.


First, install certbot:

```sh
sudo pacman -S certbot certbot-nginx
```

Now we request the certificates:

```sh
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

I got an error. The reason - I need to update my DNS to point to my own server.

I went to Namecheap, and changed from "Custom DNS" to "Namecheap Basic DNS". In "Advanced DNS" I configured the A Name Record and CNAME Record.

| Record Type  | Host          | Value              | TTL       |
|--------------|---------------|--------------------|-----------|
| A Record     | @             | 101.182.139.174    | Automatic |
| CNAME Record | www           | lachlan-miller.me. | Automatic |

Now we wait a while, and try to run the certbot command again. Once the DNS change has propogated, it should work.

It kind of did. I got a new error:

```sh
sudo certbot --nginx -d lachlan-miller.me -d www.lachlan-miller.me
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for lachlan-miller.me and www.lachlan-miller.me

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/lachlan-miller.me/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/lachlan-miller.me/privkey.pem
This certificate expires on 2025-04-27.
These files will be updated when the certificate renews.

Deploying certificate
Could not install certificate

NEXT STEPS:
- The certificate was saved, but could not be installed (installer: nginx). After fixing the error shown below, try installing it again by running:
  certbot install --cert-name lachlan-miller.me
- The certificate will need to be renewed before it expires. Certbot can automatically renew the certificate in the background, but you may need to take steps to enable that functionality. See https://certbot.org/renewal-setup for instructions.

Could not automatically find a matching server block for lachlan-miller.me. Set the `server_name` directive to use the Nginx installer.
```

I need to add some basic nginx configuration. I like to put global configuration in `/etc/nginx/nginx.conf`, and site specific in `/etc/nginx/conf.d/*`.

Top level, `/etc/nginx/nginx.conf`:

```nginx
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
	worker_connections  1024;
}

http {
	include       /etc/nginx/mime.types;
	default_type  application/octet-stream;

	log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
		'$status $body_bytes_sent "$http_referer" '
		'"$http_user_agent" "$http_x_forwarded_for"';

	access_log  /var/log/nginx/access.log  main;

	sendfile        on;
	#tcp_nopush     on;

	keepalive_timeout  65;

	#gzip  on;

	include /etc/nginx/conf.d/*.conf;
}
```

And the site specific, `/etc/nginx/conf.d/lachlan.miller.me.conf`:

```nginx
server {
    if ($host = www.lachlan-miller.me) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = lachlan-miller.me) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen 80;
        listen [::]:80;

        server_name lachlan-miller.me www.lachlan-miller.me;

        # Redirect all HTTP requests to HTTPS
        return 301 https://$host$request_uri;




}

server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name lachlan-miller.me www.lachlan-miller.me;

        # SSL configuration managed by Certbot
    ssl_certificate /etc/letsencrypt/live/lachlan-miller.me/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/lachlan-miller.me/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # Security-related options
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        location / {
                proxy_pass http://localhost:7500; # Proxy to your application
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}
```

Now it works:

```sh
sudo certbot install --cert-name lachlan-miller.me
sudo: /etc/sudo.conf is group writable
sudo: /etc/sudo.conf is group writable
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Deploying certificate
Successfully deployed certificate for lachlan-miller.me to /etc/nginx/conf.d/lachlan-miller.me.conf
Successfully deployed certificate for www.lachlan-miller.me to /etc/nginx/conf.d/lachlan-miller.me.conf
```

... kind of. My router needs to open port 443. I added these entries for IPv4 forwarding:

| Name                 | Protocol | WAN Port | LAN Port | Destination IP | Destination MAC    |
|----------------------|----------|----------|----------|----------------|--------------------|
| lachlan-https-server | TCP      | 443      | 443      | 192.168.0.130  | d8:3b:bf:30:d3:b0  |
| lachlan-server       | TCP      | 80       | 80       | 192.168.0.130  | d8:3b:bf:30:d3:b0  |

Now I see my [website](https://lachlan-miller.me), which is probably where you are reading this article!
