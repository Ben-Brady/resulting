# Resultify

Bring the rust Result and Option type into python.

```bash
pip install result-ify
```

## Result

```python
from result import Result, Ok, Err

def get_user_id() -> Result[int, str]:
    return Ok(123)

match get_user():
    case Ok(user_id):
        print(f"User ID: {user_id}")
    case Err(msg):
        print(f"Failed to get user: {msg}")
```
### Tracebacks

If you provide an exception into the Err, a traceback will be inserted.

This allows you to have the powerful debugging of Exceptions with guarentees of results


```python
from result import Err

def create_err() -> Err[str]:
    return Err("Throw Me!")

res = create_err()
res.unwrap()
```

```
Traceback (most recent call last):
  File "/example.py", line 7, in <module>
    res.unwrap()
  File "/example.py", line 6, in <module>
    res = create_err()
  File "/example.py", line 4, in create_err
    return Err("Throw Me!")
RuntimeError: Unwrapped Err(Throw Me!)
```

## Option

```python
from result import Option, Some, none

def get_user_id() -> Option[int]:
    return Some(123)

match get_user():
    case Some(user_id):
        print(f"User ID: {user_id}")
    case none():
        print(f"User does not exist")
```


## Catch Errors

You can use the `safe` decorator to catch exceptions

```python
from result import safe

@catch()
def get_user() -> str:
    raise KeyError("User Not Found")

res: Result[str, Exception] = get_user()
```

or catch specific exceptions using `catch`

```python
from result import catch

@catch([KeyError, LookupError])
def get_user() -> str:
    raise KeyError("User Not Found")

res: Result[str, KeyError|LookupError] = get_user()
```

## Optional

```python
from result import optional

@optional
def get_user() -> str|None:
    return "1"

res: Option[str] = get_user()
```
