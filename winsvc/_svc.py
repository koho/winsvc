import servicemanager
import win32service
import win32serviceutil


class Service(win32serviceutil.ServiceFramework):

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def set_service(cls, instance):
        cls._svc_name_ = instance._svc_name_
        cls._svc_display_name_ = instance._svc_display_name_
        cls._svc_description_ = instance._svc_description_
        cls._exe_name_ = instance._exe_name_
        cls._exe_args_ = instance._exe_args_
        cls.instance = instance

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPING,
            (self._svc_name_, '')
        )
        self.instance.stop()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.instance.start()

    @classmethod
    def start(cls):
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(cls)
        servicemanager.StartServiceCtrlDispatcher()
