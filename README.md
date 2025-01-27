# Backend for Vue Tools
run:
```bash
python -m venv .venv
```

```bash
source .venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

проблема с импортами:
```bash
export PYTHONPATH=$(pwd)
```
отладка:
```bash
cd app
```
```bash
python -c "import sys; print(sys.path)"
```
если выводит всякую фигню и корень то все хорошо
