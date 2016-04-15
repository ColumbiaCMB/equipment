import socket

class Hittite():
    name = 'hittite'
    def __init__(self, ipaddr=None, port=50000, terminator='\r', connect=True):
        #TODO: probably read state from the equipment eventually
        self.state = dict(output_on=False, frequency = 10.5e9, power_dBm = 0.0)
        if ipaddr:
            self.address=(ipaddr,port)
        else:
            self.address=('192.168.001.070',port)
            try:
                self.connect()
                self.disconnect()
            except socket.error:
                self.address=('192.168.0.070',port)

        self.terminator=terminator
        if connect:
            self.connect()

    def connect(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.settimeout(0.5)
        s.connect(self.address)
        self.s = s
        return
    def disconnect(self):
        self.s.close()

    def send(self,msg):
        #self.connect()
        try:
            self.s.send(msg+self.terminator)
        except Exception,e:
            print e
            raise e
        finally:
            pass
        #    self.disconnect()

    def send_and_receive(self,msg):
        try:
            self.s.send(msg+self.terminator)
            response=self.s.recv(1024)
            return response
        except Exception,e:
            print e
            raise e
        finally:
            pass

    def on(self):
        self.send('OUTP ON')
        self.state['output_on'] = True
    def off(self):
        self.send('OUTP OFF')
        self.state['output_on'] = False
    def set_freq(self,freq):
        msg='FREQ %f'%(freq)
        self.send(msg)
        self.state['frequency'] = freq
    def set_power(self,power):
        msg='POW %f'%(power)
        self.send(msg)
        self.state['power_dBm'] = power
