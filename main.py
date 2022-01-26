'''
Inspired by JetsonHacks's video about Jetson RACECAR Motor ESC Control:
https://www.youtube.com/watch?v=Mp-aSmxGAE8, last visited 26.01.2022
'''



from tkinter.constants import END
import board
import busio
import adafruit_pca9685
import tkinter as tk
import re


def decrement():
    print('Decrement')
    global dutyCycle
    dutyCycle = (dutyCycle - 1) if dutyCycle > 0 else 0
    setDutyCycle(dutyCycle)

def neutral():
    print('Reset')
    global dutyCycle
    dutyCycle = 0
    setDutyCycle(dutyCycle)

def increment():
    print('Increment')
    global dutyCycle
    dutyCycle = dutyCycle + 1
    setDutyCycle(dutyCycle)


def setDutyCycle(cycle):
    pca.channels[channel].duty_cycle = cycle
    setText(str(cycle))

def selectElement(selection):
    global channel
    print(selection)
    channel = SELECTIONLIST.index(selection)
    print(channel)

def setText(text):
    dutyCycleInput.delete(0, END)
    dutyCycleInput.insert(0, text)

def onTextChange(text):
    global dutyCycle

    if text.get() != '' and re.match('^[\d]{4}$', text.get()):
        print(text.get())
        dutyCycle = int(text.get(), base=10)
        setDutyCycle(dutyCycle) 

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c_bus = i2c, address = 0x40)
pca.frequency = 50
dutyCycle = 0
channel = 0


root = tk.Tk()
root.title('RC Car Configurator')

canvas = tk.Canvas(root, width = 620, height = 480)
canvas.pack()

SELECTIONLIST = [
    'ESC THROTTLE',
    'STEERING'
]

selectRelX = 0.35
selectRelY = 0.05

variable = tk.StringVar(root)
variable.set(SELECTIONLIST[channel])

select = tk.OptionMenu(root, variable, *SELECTIONLIST, command=selectElement)
select.config(width = 20, font = ('Helvetica', 12))
select.place(relx = selectRelX, rely = selectRelY)

buttonReverse = tk.Button(root, text = "Decrement", command=decrement)
buttonReset = tk.Button(root, text = "Reset", command=neutral)
buttonForward = tk.Button(root, text = "Increment", command=increment)

buttonRelX = 0.1
buttonRelY = selectRelY + 0.15

buttonReverse.place(relx = buttonRelX, rely = buttonRelY)
buttonReset.place(relx = buttonRelX + 1/3, rely = buttonRelY)
buttonForward.place(relx = buttonRelX + 2/3, rely = buttonRelY)

buttonRelX = 0.1
buttonRelY = 0.15

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv = sv: onTextChange(sv))

dutyCycleLabel = tk.Label(root, width = 20, text = 'Duty Cycle')
dutyCycleInput = tk.Entry(root, width = 20, validate = 'key', textvariable= sv)

dutyCycleRelX = 0.37
dutyCycleRelY = buttonRelY + 0.30

dutyCycleLabel.place(relx = dutyCycleRelX, rely = dutyCycleRelY)
dutyCycleInput.place(relx = dutyCycleRelX, rely = dutyCycleRelY + 0.05)
setText(dutyCycle)
setDutyCycle(dutyCycle)


root.mainloop()

