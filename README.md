# Resulting

Bring the rust Result and Option type into python.

```bash
pip install resulting
```

## Result

```python
from resulting import Result, Ok, Err

def get_user_id() -> Result[int, str]:
    return Ok(123)

match get_user():
    case Ok(user_id):
        print(f"User ID: {user_id}")
    case Err(msg):
        print(f"Failed to get user: {msg}")
```
### Tracebacks

When unwrapping a Result or Option, a traceback will be inserted up to the place the `Err`` was created

This allows you to have the powerful debugging of Exceptions with guarentees of results


```python
# example.py
from resulting import Err

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
from resulting import Option, Some, none

def get_user_id() -> Option[int]:
    return Some(123)

match get_user():
    case Some(user_id):
        print(f"User ID: {user_id}")
    case none():
        print(f"User does not exist")
```


## Catch Errors

You can use the `catch` decorator to catch exceptions

```python
from resulting import catch

@catch()
def get_user() -> str:
    raise KeyError("User Not Found")

res: Result[str, Exception] = get_user()
```

or catch specific exceptions using `catch`

```python
from resulting import catch

@catch([KeyError, LookupError])
def get_user() -> str:
    raise KeyError("User Not Found")

res: Result[str, KeyError|LookupError] = get_user()
```

## Optional

You can use the optional wrapper to wrap existing functions in an Option

```python
from resulting import optional

@optional
def get_user() -> str|None:
    return "1"

res: Option[str] = get_user()
```
