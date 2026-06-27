# Static Blog

A simple static site generator written in python for my own blogging pleasure.

```sh
uv sync
uv run fastapi run server.py
npm install
```

Docker:

```sh
docker build -t blog:latest .
docker run --rm -p 7777:7777 blog:latest
```

Optionally skip PDF generation during build:

```sh
docker build --build-arg SKIP_PDF=true -t blog:latest .
```

systemd (`/etc/systemd/system/fastapi.service`):

```
[Unit]
Description=Blog app (Docker)
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=lachlan
Restart=always
RestartSec=5
ExecStartPre=-/usr/bin/docker stop fastapi
ExecStartPre=-/usr/bin/docker rm fastapi
ExecStart=/usr/bin/docker run --rm --name fastapi \
  -p 7777:7777 \
  -v /opt/apps/blog:/app \
  blog:latest
ExecStop=/usr/bin/docker stop fastapi

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi

# status / logs
systemctl status fastapi
journalctl -u fastapi -f
```

