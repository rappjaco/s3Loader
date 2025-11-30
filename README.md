# Start Backend
```
uv pip install -r requirements.txt
fastapi dev main.py
```

# Start ClamAV
```
docker run -d --name clamav -p 3310:3310 -v /tmp/scan_dir:/tmp/scan_dir -v /tmp/clamd.conf:/etc/clamav/clamd.conf clamav/clamav:latest
```


# Local development
ClamAV runs in docker container and shares SCAN_DIR directory on development host system.