from abc import ABCMeta, abstractmethod


class Service:

    __metaclass__ = ABCMeta

    _svc_name_ = None
    _svc_display_name_ = None

    # Optional Attributes:
    _svc_deps_ = None        # sequence of service names on which this depends
    _exe_name_ = None        # Default to PythonService.exe
    _exe_args_ = None        # Default to no arguments
    _svc_description_ = None

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def register(self, extra_args=''):
        arg = 'svc'
        if extra_args:
            arg += ' ' + extra_args
        self._exe_args_ += ' ' + arg
        from ._svc import Service
        Service.set_service(self)

    @classmethod
    def run(cls):
        from ._svc import Service
        Service.start()
