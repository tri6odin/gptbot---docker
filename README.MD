```bash
echo "Building container..."
docker build -t gptbot .
echo "Starting container..."
docker run -d gptbot
```
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```