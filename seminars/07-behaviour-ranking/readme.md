# Behaviour Ranking

## Setup

### Step 0
Необходимо иметь установленный интерпретатор питона. Проверено для Python 3.12.3

```bash
python3 --version
> Python 3.12.3
```

Проверьте, что `pip>=19.3`

```bash
pip --version
> pip 24.0
```

```bash
python3 -m pip --version
> pip 24.0
```

иначе его стоит обновить
```bash
python -m pip install --upgrade pip
```

### Step 1
Перейти в директорию текущего семинара

### Step 2
Создать виртуальное окружение

```bash
python3 -m venv ~/.venv/07-behaviour-ranking
source ~/.venv/07-behaviour-ranking/bin/activate
pip install -r requirements.txt
```

> [PyClick](https://github.com/markovi/PyClick) собран в .whl, что позволяет удобнее его установить, без использования sudo. В requirements.txt он указан по [прямой ссылке](https://peps.python.org/pep-0440/#direct-references)

### Step 3
Запустить jupyter notebook
```bash
jupyter notebook
```
