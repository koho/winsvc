# winsvc

A Windows Service Creator API.

## Install
```
pip install winsvc
```

## Example
```python
# test_svc.py
import os
import sys
import time
import click
import pathlib
from winsvc.cmd import add_svc_command
from winsvc.svc import Service


class TestService(Service):
    _svc_name_ = 'winsvc'
    _svc_display_name_ = "WIN SVC"
    _svc_description_ = 'A Windows Service Creator'
    _exe_name_ = sys.executable

    def __init__(self, path):
        self.running = True
        self.path = path
        self._exe_args_ = f'{os.path.abspath(__file__)} {path}'

    def start(self):
        while self.running:
            pathlib.Path(self.path).touch()
            time.sleep(5)

    def stop(self):
        self.running = False


@add_svc_command()
@click.group(invoke_without_command=True)
@click.argument("path", type=click.Path())
@click.pass_context
def main(ctx, path):
    s = TestService(path)
    if ctx.invoked_subcommand is None:
        # Run in command line
        s.start()
    else:
        # Run in Windows service
        ctx.obj = s


if __name__ == '__main__':
    main()
```

**Run in command line:**
```
python test_svc.py test.txt
```

**Run in service:**
```
python test_svc.py test.txt svc -d . install
python test_svc.py test.txt svc -d . start
```
