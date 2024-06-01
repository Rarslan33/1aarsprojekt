import serial
import sys

def main():
    ports = [
        '/dev/serial0', '/dev/ttyAMA0', '/dev/ttyS0',
        '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0'
    ]

    ser = None
    for port in ports:
        try:
            ser = serial.Serial(
                port=port,         
                baudrate=9600,     
                timeout=1          
            )
            if ser.is_open:
                print(f"Serial port {port} is open")
                break
        except serial.SerialException as e:
            print(f"Failed to open serial port {port}: {e}")

    if ser is None or not ser.is_open:
        print("Failed to open any serial port")
        return

    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8',errors='ignore').rstrip()
                print(f"Received: {data}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        print("Exiting program")

    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    main()