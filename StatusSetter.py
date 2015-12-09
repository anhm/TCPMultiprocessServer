# -*- coding: UTF-8 -*-

class StatusSetter():
    def __init__(self, monitor_dic, process_num):
        self.monitor_dic = monitor_dic
        self.process_num = process_num
        self._process_status = {'status': 'init', 'process_num': process_num}
        self._update()

    def _update(self):
        self.monitor_dic[self.process_num] = self._process_status

    def start(self, remote_ip, remote_port, local_port):
        self._process_status['status'] = 'start'
        self._process_status['remote_ip'] = remote_ip
        self._process_status['remote_port'] = remote_port
        self._process_status['local_port'] = local_port
        self._update()

    def end(self):
        self._process_status['status'] = 'end'
        self._update()

    def set_start_time(self, t):
        self._process_status['start_time'] = t
        self._update()

    def set_pid(self, pid):
        self._process_status['pid'] = pid
        self._update()
