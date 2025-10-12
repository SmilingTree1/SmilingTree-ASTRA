from machine import Pin, UART
import time

uart_transmitter = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
uart_receiver = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))

def send_cmd(uart:UART, cmd:str):
    uart.write(cmd + '\r\n')
    time.sleep(0.1)
    # if uart.any():
    #     print(uart.read().decode())

# --INIT TRANSMITTER--
send_cmd(uart_transmitter, 'AT')
send_cmd(uart_transmitter,'AT+RESET')
time.sleep(1)
send_cmd(uart_transmitter, "AT+ADDRESS=1")
send_cmd(uart_transmitter, "AT+NETWORKID=5")
send_cmd(uart_transmitter, "AT+BAND=915000000")
send_cmd(uart_transmitter, "AT+PARAMETER=9,7,1,12")

# --INIT RECEIVER--
send_cmd(uart_receiver, "AT")
send_cmd(uart_receiver, "AT+RESET")
time.sleep(1)
send_cmd(uart_receiver, "AT+ADDRESS=2")
send_cmd(uart_receiver, "AT+NETWORKID=5")
send_cmd(uart_receiver, "AT+BAND=915000000")
send_cmd(uart_receiver, "AT+PARAMETER=9,7,1,12")


print("Modules initialized. Transmitting from transmitter to receiver...")

# -- TEST LOOP --
while True:
    # Send message from module 1 to module 2
    msg = "Test packet"
    send_cmd(uart_transmitter, f"AT+SEND=2,{len(msg)},{msg}")

    # Check receiver UART for incoming packets
    if uart_receiver.any():
        raw_bytes = uart_receiver.read()
        if raw_bytes is not None:  # Check if we actually got data
            raw = raw_bytes.decode().strip()
            if raw.startswith("+RCV="):
                print("Received:", raw)
    
    time.sleep(5)