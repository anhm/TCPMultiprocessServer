# -*- coding: UTF-8 -*-
import multiprocessing
import threading
import time

from StatusSetter import StatusSetter

__all__ = ['DummyProcessManager']

class DummyProcessManager(threading.Thread):
    '''
    clinet socket이 담겨 있는 queue에서 socket을 꺼내 daemon을 실행시키는 class
    한번에 하나의 daemon만을 실행함
    '''
    def __init__(self, conf, socket_queue, monitor_dic, process_num, daemon_process, param):
        '''
        @param conf: configuration
        @param socket_queue : client socket queue
        @param monitor_dic : process status save
        @param pocess_num : sequence(index) which becomes fork
        @param daemon_process: process which the server will run
        @param param: parameter where whill use from daemon_process
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
            p = multiprocessing.Process(target=DummyProcess,
                                        args=(self.monitor_dic, self.process_num,
                                              self.daemon_process, client_socket, self.param))
            p.start()

            if self.conf.get_process_time_out() >= 0:
                p.join(self.conf.get_process_time_out())
            else:
                p.join()

            try:
                client_socket.close()
            except:
                pass

            if self.terminate:
                break

    def get_process_num(self):
        return self.process_num

    def set_terminate(self, terminate=True):
        self.terminate = terminate


def DummyProcess(monitor_dic, process_num, daemon_process, client_socket, param):
    '''
    Daemon의 run을 실행시킴
    Mulitprocess에서는 Process를 상속받지 않을 경우 start를 하여도 Daemon의 run이
    자동 실행되지 않음
    '''
    status_setter = StatusSetter(monitor_dic, process_num)
    remote_ip, remote_port = client_socket.sock.getpeername()
    _, local_port = client_socket.sock.getsockname()

    status_setter.start(remote_ip, remote_port, local_port)
    daemon_process(client_socket, status_setter, param).run()
    status_setter.end()
