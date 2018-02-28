# envee
Easy abstraction for environment variables

## Python 3 only

## Usage

### Reading and writing simple variables
```python
>>> from envee import envee
>>> envee.FOO
>>> envee.all()
{'PATH': '/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
 'SHELL': '/bin/bash'}
>>> envee.FOO = "bar"
>>> envee.all()
{'PATH': '/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
 'SHELL': '/bin/bash',
 'FOO': 'bar'}
 ```

### Reading and writing python structures
```python
>>> from envee import envee
>>> envee.COMPLEX_FOO
>>> envee.all()
{'PATH': '/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
 'SHELL': '/bin/bash'}
>>> envee.COMPLEX_FOO = [{"a": [1, 2], "b": {"c": 1}}]
>>> envee.all()
{'PATH': '/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
 'SHELL': '/bin/bash',
 'COMPLEX_FOO': '[{"a": [1, 2], "b": {"c": 1}}]'}
# JSON serialized structure
>>> envee.COMPLEX_FOO
[{'a': [1, 2], 'b': {'c': 1}}]
>>> envee.COMPLEX_FOO[0]["a"] = 2
>>> envee.COMPLEX_FOO
[{'a': 2, 'b': {'c': 1}}]
>>> envee.all()["COMPLEX_FOO"]
'[{"a": 2, "b": {"c": 1}}]'
```

### Changes on a variable instance cascades back to environment
```python
>>> foo = envee.COMPLEX_FOO
>>> foo.append(1)
>>> envee.COMPLEX_FOO
[{'a': [1, 2], 'b': {'c': 1}}, 1]
 ```