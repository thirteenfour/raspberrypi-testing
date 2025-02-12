import tkinter as tk
import threading
import time
import serial
import serial.tools.list_ports
import datetime

# global variables
running = True
mega = serial.Serial()
comdev = ""
ctr = 0
connected = False
shortdate = ""

# list com ports and connect
def serial_connect():
    global connected, mega, comdev
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")
        if "Arduino" in port.description:
            comdev = port.device
            mega = serial.Serial(comdev, 9600)
            mega.reset_input_buffer()
            lbl_serial.config(text="Serial Status: Connected to " + comdev)
            connected = True
            break

# Function to update the CSV file
def updateCSV(inputline):
    update = False
    datenow = datetime.datetime.now()
    shortdate = datenow.strftime("%Y") + datenow.strftime("%m") + datenow.strftime("%d")
    filename = shortdate + ".csv"
    newline = datenow.strftime("%X") + "," + inputline[6:8] + ","
    if (inputline[9:12] == "in#"):
        newline += "in\n"
        update = True
    elif (inputline[9:13] == "out#"):
        newline += "out\n"
        update = True
    print(newline)
    if update:
        with open(filename, "a") as file:
            file.write(newline)

# Function to run the loop
def run_loop():
    global running, ctr, connected, mega
    running = True
    while running:
#         print(ctr)
#         ctr += 1
        # serial things
        if connected:
            line = mega.readline().decode('utf-8').rstrip() # receive status information from arduino
            if line[0:5] == "@iSp_":
                lbl_input.config(text="Latest input: " + line)
#                 updateCSV(line)
            print(line)
        time.sleep(0.1)
        
# Function to stop the loop
def stop_loop():
    global running, connected, mega
    running = False
    connected = False
    lbl_input.config(text="Latest input: --")
    lbl_serial.config(text="Serial Status: Disconnected")
    if mega.is_open:
        mega.close()

# Create the main window
root = tk.Tk()
root.title("Arduino Serial Test")
root.geometry('600x400')

# label for serial status
lbl_serial = tk.Label(root, text="Serial Status: Disconnected")
lbl_serial.pack()

# button for connecting to serial
btn_serial_connect = tk.Button(root, text="Connect to Serial", command=serial_connect)
btn_serial_connect.pack()

# label for serial input
lbl_input = tk.Label(root, text="Latest Input: --")
lbl_input.pack()

# Create a button to stop the loop
stop_button = tk.Button(root, text="Stop Loop", command=stop_loop)
stop_button.pack()

# Start the loop in a separate thread
loop_thread = threading.Thread(target=run_loop)
loop_thread.start()

# Run the Tkinter event loop
root.mainloop()
