from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

def setup_modbus_client(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8):
    client = ModbusSerialClient(
        method='rtu',
        port=port,
        baudrate=baudrate,
        parity=parity,
        stopbits=stopbits,
        bytesize=bytesize
    )
    return client

def read_holding_registers(client, slave_id, address, count):
    try:
        result = client.read_holding_registers(address=address, count=count, slave=slave_id)
        if not result.isError():
            return result.registers
        else:
            print(f"Error reading registers: {result}")
            return None
    except ModbusException as e:
        print(f"Modbus exception occurred: {e}")
        return None

def write_holding_register(client, slave_id, address, value):
    try:
        result = client.write_register(address=address, value=value, slave=slave_id)
        if not result.isError():
            print(f"Successfully wrote {value} to register {address}")
            return True
        else:
            print(f"Error writing to register: {result}")
            return False
    except ModbusException as e:
        print(f"Modbus exception occurred: {e}")
        return False

def main():
    client = setup_modbus_client()
    
    if not client.connect():
        print("Failed to connect to the Modbus RTU device")
        return

    try:
        # Example: Read 5 holding registers starting from address 0 from slave ID 1
        registers = read_holding_registers(client, slave_id=1, address=0, count=5)
        if registers:
            print(f"Read registers: {registers}")

        # Example: Write value 42 to holding register at address 10 of slave ID 1
        write_success = write_holding_register(client, slave_id=1, address=10, value=42)
        if write_success:
            # Read back the written value to confirm
            written_value = read_holding_registers(client, slave_id=1, address=10, count=1)
            if written_value:
                print(f"Read back written value: {written_value[0]}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
