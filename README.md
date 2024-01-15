## Quickstart

### Create a virtual environment:

```bash
# make sure version less than 3.9
python3 -m venv venv
```

`NOTE: make sure you have some free time, cause it can take a around hour or less. For me took 1 hour based on my inernet speed.`

### Install requirements:

```bash
pip install -r requirements.txt
```

### Install `ffmpeg`:

```bash
# macOS
brew install ffmpeg

# Windows
sudo apt install ffmpeg
```

### Install `fastapi`:

```bash
pip install fastapi
```

### Install `uvicorn`:

```bash
pip install uvicorn
```

### Run the server:

```bash
python3 app.py
```