from abc import ABCMeta, abstractmethod


class Service:

    __metaclass__ = ABCMeta

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
