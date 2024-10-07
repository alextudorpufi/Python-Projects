# Brute Force attack
import random
import pyautogui

chars = "abcdefghijklmnopqrstuvwxyz0123456789"
allchar = list(chars)

pword = pyautogui.password("Enter your password: ")
sample_pword = ""

while (sample_pword != pword):
    sample_pword = random.choices(allchar, k=len(pword))
    print("--" + str(sample_pword) + "--")
    if(sample_pword == list(pword)):
        print("Password Found: " + "".join(sample_pword))
        break


