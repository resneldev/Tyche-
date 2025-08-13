# Tyche (the name of the Greek goddess of randomness)
design of a mini car that moves thanks to pure random. The randomness is based on a 6-sided dice spear.
# How it work 
to carry out a movement, two throws are necessary: The first throw allows giving the direction (left or right) the second the direction (forward or backward). For the detection of the number of points on the face of the dice, a camera takes a photo of each shot and sends it to the artificial intelligence API (Chat GPT), which only returns (without comment or text) the number of points read.
### how is the value returned by the AI used?  
Depending on the roll number (first or second roll) and the value obtained, this will determine whether the car should move forward or backward, turn left or right, how many centimeters it should move forward or backward, and how many should be the turning intensity 
#### First roll: Determines the turning direction (left or right) and the turning intensity.
Note that the maximum number of points on a die is 6. 
##### *For the turning direction:*
I have assigned the first 3 values (1, 2, 3) to the left direction, and the last 3 values (4, 5, 6) to the right direction.
##### *For the intensity:* 
if the die shows a number between 1 and 3 (for the left direction), the intensity for 3 is greater than that for 2, which is greater than that for 1 (I<sub>3</sub> > I<sub>2</sub> > I<sub>1</sub>).
if the die shows a number between 4 and 6 (for the right direction), the intensity for 6 is greater than that for 5, which is greater than that for 4 (I<sub>6</sub> > I<sub>5</sub> > I<sub>4</sub>).

#### Second roll: Determines the direction of the moving (forward or backward) and the travel distance.
##### *For the moving direction:*
if the die shows a number between 1 and 3 (backward), the travel distance for 3 is greater than that for 2, which is greater than that for 1 (Td<sub>3</sub> > Td<sub>2</sub> > Td<sub>1</sub>).
if the die shows a number between 4 and 6 (forward), the travel distance for 6 is greater than that for 5, which is greater than that for 4 (Td<sub>6</sub> > Td<sub>5</sub> > Td<sub>4</sub>).
