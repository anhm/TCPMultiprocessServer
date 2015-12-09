# -*- coding: UTF-8 -*-
import multiprocessing
import threading
import time

from StatusSetter import StatusSetter
from DummyProcessManager import DummyProcessManager
from DummyThreadManager import DummyThreadManager

__all__ = ['ManagerServer', 'StatusSetter']

class ManagerServer(threading.Thread):

    def __init__(self, conf,  socket_queue, monitor_dic, daemon_process, param):
        """
        @param conf: configuration
        @param socket_queue: client socket queue
        @param monitor_dic: process status save
        @param daemon_process: process which the server whill run
        @param param: parameter where will use from daemon_process
        """
        threading.Thread.__init__(self)
        self.conf = conf
        self.socket_queue = socket_queue
        self.monitor_dic = monitor_dic
        self.daemon_process = daemon_process
        self.param = param

        self.thread_list = []
        self.process_num = 0

    def run(self):
        '''
        To confirm the max_process, prefork run
        - The case which whill increase the prefork real-time application
        - but decrease not real-time
        '''
        while True:
            count = 0
            max_process = self.conf.get_max_process()
            not_alive_list = []

            #check running process
            for thread_info in self.thread_list:
                if thread_info.is_alive():
                    count += 1
                else:
                    not_alive_list.append(thread_info)

            #remove ended process
            for not_alive in not_alive_list:
                self.monitor_dic.pop(not_alive.get_process_num())
                self.thread_list.remove(not_alive)

            #prefox-Thread
            if (max_process-count) > 0:
                for cnt in range(max_process-count):
                    process_key = self._get_process_key()
                    self.monitor_dic[process_key] = {}
                    '''
                    new_dummy_process = DummyProcessManager(self.conf, self.socket_queue, self.monitor_dic, 
                                                            process_key, self.daemon_process, self.param)
                    '''
                    new_dummy_process = DummyThreadManager(self.conf, self.socket_queue, self.monitor_dic, 
                                                            process_key, self.daemon_process, self.param)

                    new_dummy_process.setDaemon(True)
                    new_dummy_process.start()
                    self.thread_list.append(new_dummy_process)
            elif (max_process-count) < 0:
                kill_count = count - max_process
                for index, thread_info in enumerate(self.thread_list):
                    if index >= kill_count:
                        break
                    thread_info.set_terminate()

            time.sleep(1)

    def _get_process_key(self):
        self.process_num += 1
        self.process_num %= 1000
        return "Process-%04d" % self.process_num
