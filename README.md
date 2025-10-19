# Tyche (the name of the Greek goddess of randomness)
And if **Randomness** could result in physical movement? In this project, I am designing a mini car that moves purely randomly. The randomness is based on a 6-sided dice.
## The purpose of this projet
The purpose of this project is not merely to experiment with code and electronic components. Its true goal lies more in the field of the physics of consciousness than in electrical engineering.
With this project, I aim to study chaotic systems and explore the possible influence of human thought and emotion on matter. The physical theory that addresses this idea is the theory of double causality, and this project — which is more of an experimental investigation —seeks to test and demonstrate whether this theory holds true.
## How it work 
to carry out a movement, two throws are necessary: The first throw allows giving mainly the turning direction (left or right) and the second only the direction of moving (forward or backward). For the detection of the number of points on the face of the dice, a camera takes a photo of each trow and sends it to the artificial intelligence API (Chat GPT), which only returns (without comment or text) the number of points read.
### how is the value returned by the AI used
Depending on the roll number (first or second roll) and the value obtained, this will determine whether the car should move forward or backward, turn left or right, how many centimeters it should move forward or backward, and how many should be the turning intensity 
#### First roll: Determines the turning direction (left or right) and the turning intensity.
Note that the maximum number of points on a die is 6. 
##### *For the turning direction:*
I have assigned the first 2 values (1, 2) to the left direction, and the last 2 values (5, 6) to the right direction. The values 3 and 4 give the moving direction (3 for backward and 4 for forward). I made this so to assure that the car has the possibility only forward or backward after the the throws. If the first throw is only for the turning direction, it means that the car will always go left or right after any couple (two throws are necessary for the displacement) of rolls, thus I find it logical to include the backward or forward possibility in the first roll of the die.
##### *For the intensity:* 
if the die shows a number between 1 and 2 (for the left direction), the intensity for 2 is greater than that for 1 ( I<sub>2</sub> > I<sub>1</sub>).
if the die shows a number between 5 and 6 (for the right direction), the intensity for 6 is greater than that for 5 (I<sub>6</sub> > I<sub>5</sub>).

#### Second roll: Determines the direction of the moving (forward or backward) and the travel distance.
##### *For the moving direction:*
if the die shows a number between 1 and 3 (backward), the travel distance for 3 is greater than that for 2, which is greater than that for 1 (Td<sub>3</sub> > Td<sub>2</sub> > Td<sub>1</sub>).
if the die shows a number between 4 and 6 (forward), the travel distance for 6 is greater than that for 5, which is greater than that for 4 (Td<sub>6</sub> > Td<sub>5</sub> > Td<sub>4</sub>).
## How use it 
For this project, I use a Raspberry Pi 4 for the control, an LCD 1602, 3 DC motors, 2 L298N, resistors, LEDs, and an MP1584 converter. The mounting circuit is among the files. You can see all the necessary connections and do it yourself.
Open the Python code on the RPi and run it. Before starting, make sure that all dependencies are installed and that the circuit is properly assembled. To communicate with an AI API, you must create an API_KEY and save the key in a file with the extension .env. For more information, visit this link. [https://wedevs.com/blog/483810/generate-chatgpt-api-key/](https://wedevs.com/blog/483810/generate-chatgpt-api-key/)
## Dependencies
Dependencies are specified in requirements.txt for installation using pip. They include:
- numpy
- opencv-python
- python-dotenv
- openai
- RPi.GPIO
- RPLCD
