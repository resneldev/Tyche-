import os
import time
import base64
from picamera2 import Picamera2
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import cv2  # For image encoding
import RPi.GPIO as GPIO
# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(15, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(14, GPIO.LOW) 
def capture_dice_image(picam2):
    """Capture an image with Picamera2 and return numpy array"""
    image = picam2.capture_array()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

def encode_image_to_base64(image):
    """Encode numpy image to base64 JPEG"""
    _, buffer = cv2.imencode('.jpg', image)
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
                            "detail": "auto"  # ou "low"/"high" selon ton besoin
                        }
                    }
                ],
            }
        ],
        max_tokens=1,
    )
    return response.choices[0].message.content.strip()

def main():
    try:
        # Initialise la caméra UNE FOIS
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"format": "RGB888"})
        picam2.configure(config)
        picam2.start()
        time.sleep(2)  # Allow time for auto-exposure to stabilise

        while True:
            print("Capturing die image...")
            image = capture_dice_image()
        
            #save image to disk
            image_filename = "captured_dice.jpg"
            cv2.imwrite(image_filename, image)
            print(f"Image saved to {image_filename}")
        
            # Encode image and analyze        
            image_base64 = encode_image_to_base64(image)

            print("Analyzing with AI...")
            dice_value = analyze_dice_with_gpt(image_base64)

            if dice_value.isdigit() and 0 <= int(dice_value) <= 6:
                print(f"Detected die value: {dice_value}")
                
                if int(dice_value) == 4:
                    GPIO.output(14, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(14, GPIO.LOW)
                    
                if int(dice_value) == 5:
                    GPIO.output(15, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(15, GPIO.LOW)
                    
                if int(dice_value) == 6:
                    GPIO.output(18, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(18, GPIO.LOW)   
            else:
                print("Error: Unexpected value received")

    except Exception as e:
        print(f"Error: {str(e)}")
    except KeyboardInterrupt:
        print("Stop by user (Ctrl+C)")
    finally:
        picam2.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
