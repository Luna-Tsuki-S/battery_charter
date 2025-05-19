from opcua import Client, ua
import time

url = "opc.tcp://192.168.0.1:4840"

client = Client(url)



min_vol = 45
max_vol = 220

def send_data(node, data):
    opc_node = client.get_node(node)
    value = ua.DataValue(ua.Variant(data, ua.VariantType.Float))
    opc_node.set_value(value)
    return f"node{node}, Data sent: {value}"


def get_data(node):
    opc_node = client.get_node(node)
    vals = opc_node.get_value()
    return vals
    
def simulate_voltage_change(ida_volt, now_volt, per):
    change = now_volt * per
    if ida_vol > now_vol:
        new_voltage = now_volt * (1+per)
    else:
        new_voltage = now_volt * (1-per)
    return new_voltage


while True:
    ida_vol = 90
    now_vol = 80
    try:
        client.connect()

        data = get_data(("ns=4;i=4"))

        per = data / 27648
        print(f'{data}, {per}')

        now_vol = simulate_voltage_change(ida_vol, now_vol, per)
        
        if now_vol > max_vol:
            now_vol = max_vol
        elif now_vol < min_vol:
            now_vol = min_vol
        else:
            now_vol = now_vol

        send_data("ns=4;i=2", ida_vol)
        send_data("ns=4;i=3", now_vol)
        print(f"IDa_vol: {ida_vol}, Now_vol: {now_vol}")

    
    finally:
        client.disconnect()

    time.sleep(1)