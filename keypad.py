import RPi.GPIO as GPIO

# Keyboard variables

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_keypad():
    keys = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]
    lines = [L1, L2, L3, L4]
    columns = [C1, C2, C3, C4]
    output = ""
    for i, line in enumerate(lines):
        GPIO.output(line, GPIO.HIGH)
        for j, column in enumerate(columns):
            if GPIO.input(column) == 1:
                output = keys[i][j]
                print(output)
        GPIO.output(line, GPIO.LOW)
    return output 

