from OPC_PLC import OPC_UA_CONNECTION
from scipy.spatial.distance import cosine
import numpy as np

def main(now_vol):
    while True:
        all_the_mode = np.array([115, 57.5, 45])
        url = "opc.tcp://192.168.0.1:4840"
        ida_vol = 0
        now_vol = now_vol

        #decision from PPO
        act = decision()

        match act:
            case 0:
                ida_vol = now_vol
            case 1:
                now_vol += 5
            case 2:
                now_vol -= 5

        now_vol_array = np.identity(3) * now_vol

        cos = []
        for i in range(3):
            row = now_vol_array[i, :]
            similarity = np.dot(row, all_the_mode) / (np.linalg.norm(row) * np.linalg.norm(all_the_mode))
            cos.append(similarity)

        indx_volt = np.argmax(cos)
        ida_vol = all_the_mode[indx_volt]

        # Create instance of OPC_UA_CONNECTION
        opc_connection = OPC_UA_CONNECTION(ida_vol, now_vol, url)

        # Start the connection
        if not opc_connection.connection():
            print("Connection completed")