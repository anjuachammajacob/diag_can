import can
import isotp
import udsoncan
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs

class TestCodec(udsoncan.DidCodec):
    def encode(self, val):
        return val
    def decode(self, val):
        return val
    def __len__(self):
        return 33
    
# Configure CAN interface (adjust channel as needed)
can_bus = can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000)
isotp_params = {
    'stmin' : 5,
    'blocksize' : 8,
    'wftmax' : 0,
    'tx_padding' : 0xAA,
    'rx_flowcontrol_timeout' : 1000,
    'rx_consecutive_frame_timeout' : 1000,
}
# Define ISO-TP layer
address = isotp.Address(isotp.AddressingMode.Normal_29bits, 0x18DA27F0, 0x18DAF027)
stack = isotp.CanStack(bus=can_bus, address=address, params = isotp_params)
conn = PythonIsoTpConnection(stack)
config = dict(udsoncan.configs.default_client_config)
config['data_identifiers'] = {
    0xF1C1: TestCodec
}
try:
    with Client(conn, config=config) as client:
        try:
            response = client.read_data_by_identifier(0xF1C1)
            if response.code == 0:
                print(response, response.data, 'pos response')
            else:
                print(response, 'neg response')
        except Exception as e:
            print(e)
except Exception as e:
    print(f"An error occured: {e}")
finally:
    can_bus.shutdown()

