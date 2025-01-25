+++
title: Installing Custom TLS Certs, Allowing IP Forwarding on Arch
published: 2025-01-25
description: I moved to Arch Linux recently, and learned how to install custom TLS certificates, and allow IPv4 forwarding.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

## Custom Certificates

On Ubuntu, you can install a custom certificate like this:

```sh
sudo apt install -yy ca-certificates
sudo cp microba-root-ca.crt /usr/local/share/ca-certificates/
ls -aFlh /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

Arch Linux uses a different command, `update-ca-trust`, which is part of `ca-certificates-utils`.

```sh
sudo pacman -S ca-certificates-utils
```

Next, place your certificate in `/etc/ca-certificates/trust-sources/anchors`

```sh
sudo cp your-root-ca.crt /etc/ca-certificates/trust-source/anchors/
``

And update the trusted certificates using:

```sh
sudo update-ca-trust
```

Finally, run `trust list` and you should see your certificate there.

## Allow IPv4 Forwarding

This was also required to access my internal work network, which requires a VPN (Tailscale) and a custom root certificate.

I ran:

```sh
sysctl net.ipv4.ip_forward
```

Which was set to 0. I needed to enable it!

You can temporarily do it like this:

```sh
sudo sysctl -w net.ipv4.ip_forward=1
```


Better yet, make it permanent:

```sh
sudo nvim /etc/sysctl.d/99-sysctl.conf
# add this
net.ipv4.ip_forward=1
# restart
sudo sysctl --system
```

Arch is great - you need to learn how things work, but this really forces you to understand what's going on. I like it. 
