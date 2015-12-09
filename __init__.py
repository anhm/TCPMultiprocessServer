# -*- coding: UTF-8 -*-
import Queue
import multiprocessing
import M6.Common.Protocol.Socket as Socket
import time

from ServerConf import ServerConf
from MoniterServer import MoniterServer
from ManagerServer import ManagerServer

__all__ = ['Server']

class Server():
    def __init__(self, server_port, monitor_port, daemon_process, param=None,
                 max_process=3, process_time_out=-1, server_name=None):
        """
        @param server_port: running server port
        @param monitor_port: process moniter port
        @param daemon_process: running process module
        @param param: parameter use at daemon_process
        @param max_process: number of simutaneously runing process
        @prarm process_time_out: number of process time out
               (process의 join parameter로 사용)
               < 0: (Default) when ending until
               = 0: not join
               > 0: wait time
               WARNING -todo...-
        @param server_name: monitmoniter에 표시할 server이름
               None: (Default) daemon_process에서 class이름을 확인하여 사용
        """

        #Use ManagerServer
        self.daemon_process = daemon_process
        self.socket_queue = Queue.Queue()
        self.param = param

        #Use MoniterServer
        self.monitor_dic = multiprocessing.Manager().dict()

        if server_name is None:
            server_name = daemon_process.__name__

        #Setup Server Conf
        self.conf = ServerConf(server_port, monitor_port,
                               server_name, max_process, process_time_out)

    def run(self):
        #start monitor
        if self.conf.get_monitor_port() != 0:
            monitor_server = MoniterServer(self.conf, self.monitor_dic, self.socket_queue)
            monitor_server.setDaemon(True)
            monitor_server.start()

        #start process manager
        manager_server = ManagerServer(self.conf, self.socket_queue, self.monitor_dic,
                                       self.daemon_process, self.param)
        manager_server.setDaemon(True)
        manager_server.start()

        self.sock = Socket.Socket()
        self.sock.Bind(self.conf.get_server_port())
        while True:
            client_sock = self.sock.Accept()
            if not client_sock:
                break

            print 'put', time.time()
            self.socket_queue.put(client_sock)

if __name__ == '__main__':
    class Test():
        def __init__(self, socket, monitor, param):
            import os
            monitor.set_start_time('111111')
            monitor.set_pid(os.getpid())

        def run(self):
            import time
            time.sleep(5)
            pass

    #def __init__(self, server_port, monitor_port, daemon_process, param=None,
    #             max_process=3, process_time_out=-1, server_name=None):
    Server(5001, 5002, Test, 'TestClass', 
           1, -1, None).run()
