# Static Blog

A simple static site generator written in python for my own blogging pleasure.

```sh
uv python install 3.12
uv python pin 3.12
uv pip install -e .
uv run fastapi run server.py
```

systemd:

```
[Unit]
Description=FastAPI app (uv + FastAPI)
After=network.target

[Service]
Type=simple
User=lachlan
WorkingDirectory=/opt/apps/blog
ExecStart=/home/lachlan/.local/bin/uv run fastapi run server.py --port 7777
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

In `/etc/systemd/system/fastapi.service`

```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi

###

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart fastapi

### 

systemctl status fastapi
journalctl -u fastapi -f
```

