# -*- coding: UTF-8 -*-
import threading
import time

from StatusSetter import StatusSetter

__all__ = ['DummyThreadManager']

class DummyThreadManager(threading.Thread):
    def __init__(self, conf, socket_queue, monitor_dic, process_num, daemon_process, param):
        '''
        @param conf: configuration
        @param socket_queue: client socket queue
        @param monitor_dic: process status save
        @param pocess_num: sequence(index) which becomes fork
        @param daemon_process: process which the server will run
        @param param: parameter where will use from daemon_process
        '''
        threading.Thread.__init__(self)
        self.conf = conf
        self.socket_queue = socket_queue
        self.monitor_dic = monitor_dic
        self.daemon_process = daemon_process
        self.process_num = process_num
        self.param = param

        #prefork의 개수를 줄일 경우 스스로 종료되기 위한 status
        self.terminate = False

    def run(self):
        while True:
            client_socket = self.socket_queue.get()

            st = time.time()

            status_setter = StatusSetter(self.monitor_dic, self.process_num)
            remote_ip, remote_port = client_socket.sock.getpeername()
            _, local_port = client_socket.sock.getsockname()

            status_setter.start(remote_ip, remote_port, local_port)
            self.daemon_process(client_socket, status_setter, self.param).run()
            status_setter.end()

            if self.terminate:
                break

    def get_process_num(self):
        return self.process_num

    def set_terminate(self, terminate=True):
        self.terminate = terminate
