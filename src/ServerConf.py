

class ServerConf():
    _server_port = None
    _monitor_port = None
    _server_name = None
    _max_process = None
    _process_time_out = None

    def __init__(self, server_port, monitor_port, 
                 server_name, max_process, process_time_out):
        self._server_port = server_port
        self._monitor_port = monitor_port
        self._server_name = server_name
        self._max_process = max_process
        self._process_time_out = process_time_out

    def get_server_port(self):
        return self._server_port

    def get_monitor_port(self):
        return self._monitor_port

    def set_server_name(self, server_name):
        self._server_name = server_name

    def get_server_name(self):
        return self._server_name

    def set_max_process(self, max_process):
        self._max_process = max_process

    def get_max_process(self):
        return self._max_process

    def set_process_time_out(self, process_time_out):
        self._process_time_out = process_time_out

    def get_process_time_out(self):
        return self._process_time_out
        
