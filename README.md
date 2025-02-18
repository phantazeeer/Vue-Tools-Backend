# Backend for Vue Tools
run:
```bash
python -m venv .venv
```

```bash
source .venv/Scripts/activate
```

```bash
pip install -r requirements/dev.txt
```
проблема с импортами:
```bash
export PYTHONPATH=$(pwd)
```
проверить их:
```bash
python -c "import sys; print(sys.path)"
```