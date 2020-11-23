import os

import click

_install_update_options = [
    click.option('--username', help='The Username the service is to run under'),
    click.option('--password', help='The password for the username'),
    click.option('--startup', type=click.Choice(['manual', 'auto', 'disabled', 'delayed'], case_sensitive=False),
                 help='How the service starts, default = manual'),
    click.option('--interactive', is_flag=True, help='Allow the service to interact with the desktop.'),
    click.option('--perfmonini', type=click.File(), help='.ini file to use for registering performance monitor data'),
    click.option('--perfmondll', type=click.File(), help='.dll file to use when querying the service for'
                                                         'performance data, default = perfmondata.dll')
]

_start_stop_options = [
    click.option('--wait', type=int, help='Wait for the service to actually start or stop. '
                                          'If you specify --wait with the \'stop\' option, the service'
                                          'and all dependent services will be stopped, each waiting'
                                          'the specified period.')
]


def pass_arg(argv):
    import win32serviceutil
    from ._svc import Service
    win32serviceutil.HandleCommandLine(Service, argv=argv)


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def add_svc_command(svc_main=lambda ctx: ctx.obj.run()):
    def _svc_command(func):
        svc.__svc_main__ = svc_main
        func.add_command(svc)
        return func
    return _svc_command


@click.group(invoke_without_command=True)
@click.option("--wd", "-d", type=click.Path(), help="Working directory")
@click.pass_context
def svc(ctx, wd):
    extra_args = ''
    if wd:
        path = os.path.abspath(wd)
        assert os.path.exists(path)
        extra_args += f'--wd={path}'
        os.chdir(path)
    ctx.obj.register(extra_args)
    if ctx.invoked_subcommand is None and callable(svc.__svc_main__):
        svc.__svc_main__(ctx)


@svc.command()
@add_options(_install_update_options)
def install(**kwargs):
    interactive = kwargs.pop('interactive')
    argv = [''] + [f'--{k}={v}' for k, v in kwargs.items() if v is not None]
    if interactive:
        argv.append('--interactive')
    argv.append('install')
    pass_arg(argv)


@svc.command()
@add_options(_install_update_options)
def update(**kwargs):
    interactive = kwargs.pop('interactive')
    argv = [''] + [f'--{k}={v}' for k, v in kwargs.items() if v is not None]
    if interactive:
        argv.append('--interactive')
    argv.append('update')
    pass_arg(argv)


@svc.command()
def remove():
    argv = ['', 'remove']
    pass_arg(argv)


@svc.command()
@add_options(_start_stop_options)
def start(**kwargs):
    argv = [''] + [f'--{k}={v}' for k, v in kwargs.items() if v is not None] + ['start']
    pass_arg(argv)


@svc.command()
@add_options(_start_stop_options)
def restart(**kwargs):
    argv = [''] + [f'--{k}={v}' for k, v in kwargs.items() if v is not None] + ['restart']
    pass_arg(argv)


@svc.command()
@add_options(_start_stop_options)
def stop(**kwargs):
    argv = [''] + [f'--{k}={v}' for k, v in kwargs.items() if v is not None] + ['stop']
    pass_arg(argv)


@svc.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def debug(args):
    argv = ['', 'debug'] + list(args)
    pass_arg(argv)
