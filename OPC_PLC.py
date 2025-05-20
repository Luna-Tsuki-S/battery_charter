from opcua import Client, ua
import time
from scipy.spatial.distance import cdist
import numpy
# url = "opc.tcp://192.168.0.1:4840"

# client = Client(url)
#  # _ida_volt = 90
#  # now_vol = 80
class OPC_UA_CONNECTION():
    def __init__(self, ida_volt, now_volt, url):
        self.min_vol = 45
        self.max_vol = 114
        self.now_volt = now_volt
        self.ida_volt = ida_volt
        self.url = url
        self.client = Client(self.url)

    def send_data(self,node, data):
        opc_node = self.client.get_node(node)
        value = ua.DataValue(ua.Variant(data, ua.VariantType.Float))
        opc_node.set_value(value)
        return f"node{node}, Data sent: {value}"


    def get_data(self, node):
        opc_node = self.client.get_node(node)
        vals = opc_node.get_value()
        return vals
    
    @property
    def now_vol(self):
        return self._now_vol

    @property
    def _ida_volt(self):
        return self._ida_volt

    @now_vol.setter
    def simulate_voltage_change(self, N_V, I_V, per):
        change = N_V * self.per
        if self.I_V > self.N_V:
            new_voltage = self.N_V * (1+self.per)
        else:
            new_voltage = self.N_V * (1-self.per)
        
        if new_voltage > self.max_vol:
            new_voltage = self.max_vol
        elif new_voltage < self.min_vol:
            new_voltage = self.min_vol
        else:
            new_voltage
        self._now_vol = new_voltage

    @_ida_volt.setter
    def _ida_volt(self, value):
        self._ida_volt = value


    def connection(self):
        while True:
            try:
                
                self.client.connect()

                data = self.get_data(("ns=4;i=4"))
                self.per = data / 27648
                
                print(f'{data}, {self.per}')

                self.simulate_voltage_change(self._ida_volt, self._now_vol, self.per)
                
                # if self.now_vol > self.max_vol:
                #     self.now_vol = self.max_vol
                # elif self.now_vol < self.min_vol:
                #     self.now_vol = self.min_vol
                # else:
                #     self.now_vol

                self.send_data("ns=4;i=2", self._ida_volt)
                self.send_data("ns=4;i=3", self._now_vol)
                print(f"_ida_volt: {self._ida_volt}, Now_vol: {self._now_vol}")

            
            finally:
                
                cos =  self._now_vol / self._ida_volt
                if cos > 0.005:
                    self.client.disconnect()
                    return 0
                    break
                

            time.sleep(1)