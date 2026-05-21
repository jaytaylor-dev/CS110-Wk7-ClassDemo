# Without classes, keeping related data together is clumsy. If we want to track

# several dogs, the name and energy of each float around in separate variables

# (or parallel lists) that we have to keep lined up by hand.

# The CityModel class in the predictive-policing demo has the exact same shape:

#

# class CityModel:

# def **init**(self): # sets up the districts (the data)

# ...

# def step(self): # runs one round (the behavior)

# ...

#

# Once students see that **init** = "set up the starting data" and a method =

# "an action the object can take," the simulator stops looking like magic and

# starts looking like a Dog that happens to model a city.

#

# The list-of-objects idea from PART 4-5 also carries over: anywhere a program

# needs to manage MANY of the same kind of thing (dogs, districts, students,

# loan applicants...), the pattern is the same — one class as the blueprint,

# one list to hold the instances, and a loop to work through them.

# PREDICTIVE POLICING: A FEEDBACK LOOP DEMO

A teaching tool for a computing ethics class studying Cathy O'Neil's
"Weapons of Math Destruction."

THE CORE IDEA (O'Neil, Ch. 5 "Civilian Casualties: Justice in the Age
of Big Data"):

A predictive policing model does NOT measure crime.
It measures _recorded_ crime --- arrests, citations, stops.
Recorded crime depends on where police look.
Where police look depends on the model.

So the model's "predictions" become self-fulfilling. A district
flagged as high-risk gets more patrols, more patrols find more
low-level offenses, those offenses feed back into the model as
proof the district was high-risk all along. The loop tightens.

THE SETUP:
Two neighborhoods, A and B, with IDENTICAL true underlying crime.
We seed the model with a tiny, arbitrary initial bias toward A
(imagine a single noisy data point, or a historical prejudice).
Then we just let the loop run. Press the button and watch.

Nothing about the neighborhoods differs. Only the model's
attention differs --- and that turns out to be enough.
