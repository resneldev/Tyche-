import os
import time
import base64
from picamera2 import Picamera2
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import cv2  # For image encoding
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time
# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
roll_number=0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Motor 1
M1_IN1, M1_IN2, M1_EN = 17, 27, 18

#Motor 2
M2_IN1, M2_IN2, M2_EN = 22, 23, 19

#Motor 3
M3_IN1, M3_IN2, M3_EN = 5, 6, 13

#list for initialisation
pins = [M1_IN1, M1_IN2, M1_EN,
        M2_IN1, M2_IN2, M2_EN,
        M3_IN1, M3_IN2, M3_EN]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Set up PWM for motor control
pwm1 = GPIO.PWM(M1_EN, 1000)
pwm2 = GPIO.PWM(M2_EN, 1000)
pwm3 = GPIO.PWM(M3_EN, 1000)

# Start PWM with 0% duty cycle
pwm1.start(0)  
pwm2.start(0)  
pwm3.start(0)  
    
# Configuration in 4-bit mode
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19,
              pins_data=[13, 6, 5, 11],
              numbering_mode=GPIO.BCM)

def capture_dice_image(picam2):
    """Capture an image with Picamera2 and return numpy array"""
    image = picam2.capture_array()
    
    return image

def encode_image_to_base64(image):
    """Encode numpy image to base64 JPEG"""
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', image_bgr)
    return base64.b64encode(buffer).decode('utf-8')

def analyze_dice_with_gpt(image_base64):
    """Analyze image with GPT-4 Vision to detect dice value"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "This image shows a standard die (or dice). "
                            "If you clearly see a die, count the dots visible on its top face "
                            "and respond ONLY with that number (1-6). "
                            "If no die is visible or recognizable in the image, respond ONLY with the number 0. "
                            "Be accurate. Count carefully, especially when the face shows six dots."
                            "Return just the number with no explanation take the necessary time to count well the black spots on the face of dice."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "auto"  # or "low"/"high" depending on your needs
                        }
                    }
                ],
            }
        ],
        max_tokens=1,
    )
    return response.choices[0].message.content.strip()

def do_action(dice_value):
        if dice_value.isdigit() and 0 <= int(dice_value) <= 6:
            print(f"Detected die value: {dice_value}")

            if(roll_number ==1):    
                lcd.clear()
                lcd.write_string("turning direction") 
                print("Turning direction") 
                if int(dice_value) == 0:
                    lcd.clear()
                    lcd.write_string("   no dice         detected")        

                if(int(dice_value) == 1 or int(dice_value) == 2 ):
                    lcd.clear()
                    lcd.write_string("tunrning in the     left direction")
                    print("Turning left direction")
                    lcd.clear()
                    lcd.write_string("left direction")
                    if int(dice_value) == 1:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 50%")
                        GPIO.output(M1_IN1, GPIO.LOW)
                        GPIO.output(M1_IN2, GPIO.HIGH)
                        GPIO.output(M2_IN1, GPIO.HIGH)
                        GPIO.output(M2_IN2, GPIO.LOW)                        
                        pwm2.ChangeDutyCycle(50)
                        pwm1.ChangeDutyCycle(50)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    # If the dice value is 2, we will turn left with 100% intensity
                    if int(dice_value) == 2:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 100%")
                        GPIO.output(M1_IN1, GPIO.LOW)
                        GPIO.output(M1_IN2, GPIO.HIGH)
                        GPIO.output(M2_IN1, GPIO.HIGH)
                        GPIO.output(M2_IN2, GPIO.LOW)
                        pwm2.ChangeDutyCycle(100)
                        pwm1.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
                # If the dice value is 5 or 6, we will turn in the right direction
                # If the dice value is 5, we will turn right with 50% intensity
                if(int(dice_value) == 5 or int(dice_value) == 6):
                    lcd.clear()
                    lcd.write_string("turning in the     right direction")
                    print("Turning right direction")
                    lcd.clear()
                    lcd.write_string("right direction")

                    if int(dice_value) == 5:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 50%")
                        GPIO.output(M1_IN1, GPIO.HIGH)
                        GPIO.output(M1_IN2, GPIO.LOW)       
                        GPIO.output(M2_IN1, GPIO.LOW)
                        GPIO.output(M2_IN2, GPIO.HIGH)
                        pwm1.ChangeDutyCycle(50)
                        pwm2.ChangeDutyCycle(50)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    # If the dice value is 6, we will turn right with 100% intensity
                    if int(dice_value) == 6:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 100%")
                        GPIO.output(M1_IN1, GPIO.HIGH)
                        GPIO.output(M1_IN2, GPIO.LOW)
                        GPIO.output(M2_IN1, GPIO.LOW)
                        GPIO.output(M2_IN2, GPIO.HIGH)
                        pwm1.ChangeDutyCycle(100)
                        pwm2.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
                if(int(dice_value) == 3 or int(dice_value) == 4):
                    lcd.clear()
                    lcd.write_string("for/backward")
                    print("Forward/Backward direction")
                    if int(dice_value) == 3:
                        lcd.clear()
                        lcd.write_string("backward           direction")
                        print("Backward direction")
                        move_backward()
                        pwm1.ChangeDutyCycle(100)
                        pwm2.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
                    # If the dice value is 4, we will move forward with 100% intensity
                    if int(dice_value) == 4:
                        lcd.clear()
                        lcd.write_string("forward            direction")  
                        print("Forward direction")
                        move_forward()
                        pwm1.ChangeDutyCycle(100)
                        pwm2.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
            # For the second roll, we will move in a direction based on the dice value
            if(roll_number == 2):
                lcd.clear()
                lcd.write_string("moving direction")
                print("Moving direction")
                if int(dice_value) == 0:
                    lcd.clear()
                    lcd.write_string("   no dice         detected")
                if(int(dice_value) == 1 or int(dice_value) == 2 or int(dice_value) == 3):
                    lcd.clear()
                    lcd.write_string("moving backward     direction")
                    print("Moving backward direction")
                    lcd.clear()
                    lcd.write_string("backward :")
                    if int(dice_value) == 1:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 33,3%")
                        move_backward()
                        pwm2.ChangeDutyCycle(50)
                        pwm1.ChangeDutyCycle(50)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    # If the dice value is 2, we will move backward with 66.6
                    if int(dice_value) == 2:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity  66,6%")
                        move_backward()
                        pwm2.ChangeDutyCycle(75)
                        pwm1.ChangeDutyCycle(75)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    # If the dice value is 3, we will move backward with 100% intensity
                    if int(dice_value) == 3:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 100%")
                        move_backward()
                        pwm2.ChangeDutyCycle(100)
                        pwm1.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
                if(int(dice_value) == 4 or int(dice_value) == 5 or int(dice_value) == 6):
                    lcd.clear()
                    lcd.write_string("moving forward     direction")
                    print("Moving forward direction")
                    lcd.clear()
                    lcd.write_string("forward :")
                    if int(dice_value) == 4:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 33,3%")
                        move_forward()                       
                        pwm2.ChangeDutyCycle(50)
                        pwm1.ChangeDutyCycle(50)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    if int(dice_value) == 5:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity  66,6%")
                        move_forward()                       
                        pwm2.ChangeDutyCycle(75)
                        pwm1.ChangeDutyCycle(75)
                        time.sleep(1)  # Allow time for the motor to turn
                        stop_motors()
                    if int(dice_value) == 6:
                        lcd.cursor_pos = (0, 1)
                        lcd.write_string("intensity 100%")
                        move_forward()                       
                        pwm2.ChangeDutyCycle(100)
                        pwm1.ChangeDutyCycle(100)
                        time.sleep(2)  # Allow time for the motor to turn
                        stop_motors()
                roll_number = 0  # Reset roll number after the second roll
        else:
                print("Error: Unexpected value received")    
def stop_motors():
    """Sets all M1 and M2 pins to LOW to stop the motors"""
    GPIO.output(M1_IN1, GPIO.LOW)
    GPIO.output(M1_IN2, GPIO.LOW)
    GPIO.output(M2_IN1, GPIO.LOW)
    GPIO.output(M2_IN2, GPIO.LOW)
def move_forward():
    """Sets M1 and M2 to move forward"""
    GPIO.output(M1_IN1, GPIO.HIGH)
    GPIO.output(M1_IN2, GPIO.LOW)
    GPIO.output(M2_IN1, GPIO.HIGH)
    GPIO.output(M2_IN2, GPIO.LOW)
def move_backward():
    """Sets M1 and M2 to move backward"""
    GPIO.output(M1_IN1, GPIO.LOW)
    GPIO.output(M1_IN2, GPIO.HIGH)
    GPIO.output(M2_IN1, GPIO.LOW)
    GPIO.output(M2_IN2, GPIO.HIGH)
def main():
    try:
        # Initialize the camera ONCE
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"format": "RGB888"})
        picam2.configure(config)
        picam2.start()
        time.sleep(2)  # Allow time for auto-exposure to stabilise

        while True:
            print("Rolling the dice...")
            lcd.clear()
            lcd.write_string("Rolling the dice...")
            GPIO.output(M3_IN1, GPIO.HIGH)
            GPIO.output(M3_IN2, GPIO.LOW)
            pwm3.ChangeDutyCycle(100)
            lcd.clear()
            lcd.write_string(f"  Rolling...{roll_number}")
            time.sleep(2)  # Allow time for the motor to spin
            GPIO.output(M3_IN1, GPIO.LOW)
            GPIO.output(M3_IN2, GPIO.LOW)
            pwm3.ChangeDutyCycle(0)  # Stop the motor
            lcd.clear()
            roll_number += 1
            image = capture_dice_image(picam2)
            lcd.write_string(f"Image captured")  

            #save image to disk
            print("Saving image to disk...")
            lcd.clear()
            lcd.write_string("Saving image...")
            image_filename = "captured_dice.jpg"
            cv2.imwrite(image_filename, image)
            print(f"Image saved to {image_filename}")
            lcd.clear()
            lcd.write_string("   Analyzing...")
        
            # Encode image and analyze        
            image_base64 = encode_image_to_base64(image)
            lcd.clear()
            lcd.write_string("   Analyzing        with AI...")
            print("Analyzing with AI...")
            dice_value = analyze_dice_with_gpt(image_base64)
            
            lcd.cursor_pos = (0, 1)
            lcd.write_string(" " * 16)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(" " * 16)
            lcd.cursor_pos = (0, 1)
            
            do_action(dice_value)

    except Exception as e:
        print(f"Error: {str(e)}")
    except KeyboardInterrupt:
        print("Stop by user (Ctrl+C)")
    finally:
        picam2.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()