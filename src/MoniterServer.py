# -*- coding: UTF-8 -*-
import threading
import M6.Common.Protocol.Socket as Socket

__all__=['MoniterServer']

class MoniterServer(threading.Thread):
    def __init__(self, conf, monitor_dic, socket_queue):
        '''
        @parm conf: configuration
        @param monitor_dic: process status save
        '''
        threading.Thread.__init__(self)
        self.conf = conf
        self.monitor_dic = monitor_dic
        self.socket_queue = socket_queue

    def run(self):
        '''
        accept at the time of crate new thread
        '''
        sock = Socket.Socket()
        sock.Bind(self.conf.get_monitor_port())
        while True:
            client_socket = sock.Accept()
            print client_socket
            if not client_socket:
                break

            process_monitor = ProcessMoniter(self.conf, client_socket, self.monitor_dic, self.socket_queue)
            process_monitor.setDaemon(True)
            process_monitor.start()


class ProcessMoniter(threading.Thread):

    def __init__(self, conf, monitor_sock, monitor_dic, socket_queue):
        '''
        @param conf: configuration
        @param monitor_sock: connectied client socket
        @param monitor_dic: process status save
        @param socket_queue: socket_queue
        '''
        threading.Thread.__init__(self)
        self.conf = conf
        self.monitor_sock = monitor_sock
        self.monitor_dic = monitor_dic
        self.socket_queue = socket_queue

        self.protocol_dic = {'QUIT': self._quit,
                             'GET_PROCESS_STATUS': self._get_process_status,
                             'SET_MAX_PROCESS': self._set_max_process,
                             'GET_MAX_PROCESS': self._get_max_process,
                             'GET_QUEUE_SIZE': self._get_queue_size,
                             'GET_ALL': self._all}

    def run(self):
        self.monitor_sock.SendMessage("WELCOM %s\r\n" % self.conf.get_server_name())
        while True:
            line = self.monitor_sock.Readline().strip().split(' ', 1)
            if line[0] in self.protocol_dic:
                if len(line) == 2:
                    result_message = self.protocol_dic[line[0]](line[1])
                else:
                    result_message = self.protocol_dic[line[0]]()
            else:
                result_message = 'NotSupport\r\n'

            self.monitor_sock.SendMessage(result_message)
            if line[0] == 'QUIT':
                break

        try:
            self.monitor_sock.close()
        except:
            pass

    def _quit(self):
        '''
        QUIT
        '''
        return 'BYE\r\n'

    def _all(self):
        '''
        GET_ALL
        '''
        for process_num in self.monitor_dic.keys():
            print "%s:%s" % (process_num, self.monitor_dic[process_num])
        return "OK\r\n"

    def _get_queue_size(self):
        '''
        GET_QUEUE_SIZE
        '''
        queue_size = self.socket_queue.qsize()
        return "OK %s\r\n" % queue_size

    def _get_process_status(self):
        '''
        GET_POOL_COUNT
        '''
        return "%s\r\n" % multiprocessing.active_children()

    def _set_max_process(self, param):
        '''
        SET_MAX_PROCESS {process_count}
        '''
        self.monitor_dic['max_process'] = int(param)
        return 'OK\r\n'

    def _get_max_process(self):
        '''
        GET_MAX_PROCESS
        '''
        return 'OK %s \r\n' % self.monitor_dic['max_process']

