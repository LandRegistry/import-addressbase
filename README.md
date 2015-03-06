# Setup

To create a virtual env, run the following from a shell:

```
    mkvirtualenv -p /usr/bin/python3 import-addressbase
    pip install -r requirements.txt
    pip install -r requirements_test.txt
```

To run it, run the following from a shell:

```
    workon import-addressbase
    python import.py /path/to/addressbase_file.csv -n localhost:4900
```

To test, run the following:
```
    python run_tests.py
```
