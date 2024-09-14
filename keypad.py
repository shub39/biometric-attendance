import RPi.GPIO as GPIO
from constants import PASSCODE
import time

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
        GPIO.output(line, GPIO.LOW)
    return output 

def enter_passcode():
    time.sleep(0.3)
    input_code = ""
    print("[VERIFY] Enter your 4-digit passcode:")
    
    while len(input_code) < 4:
        key = None
        while not key:
            key = read_keypad()
            time.sleep(0.3)

        if key:
            print(f"[VERIFY] Key pressed: {key}")
            if key.isdigit():
                input_code += key
                print(f"[VERIFY] Current input: {input_code}")
            elif key == "*":
                input_code = ""
                print("[VERIFY] Input reset.")
    
    return input_code

def enter_roll():
    number = ""
    
    while len(number) < 2:
        print("[DD] ENTER NUMBER:")
        key = None
        while not key:
            key = read_keypad()
            time.sleep(0.2)

        if key:
            if key.isdigit():
                number += key
                print(f"[DD] CURRENT NUMBER: {number}")
            elif key == "*":
                number = ""
                print("[DD] NUMBER RESET.")
    
    return number

def roll_list():
    numbers_list = []

    while True:
        two_digit_number = enter_roll()
        numbers_list.append(two_digit_number)
        print(f"\n[DD] ROLL ADDED: {two_digit_number}")
        
        while True:
            print("[DD] Press 'A' to add another number, 'B' to finish.")
            choice = None
            while not choice:
                choice = read_keypad()
                time.sleep(0.1)

            if choice == "A":
                print("[DD] Adding another roll.")
                break
            elif choice == "B":
                print("[DD] Finished adding rolls.\n")
                return numbers_list
            else:
                continue

def verify_passcode():
    entered_code = enter_passcode()
    if entered_code == PASSCODE:
        print("[VERIFY] ACCESS GRANTED.")
        return True
    else:
        print("[VERIFY] ACCESS DENIED.")
        return False
