"""
Intro to Classes — a live-coding demo
=====================================
A short, run-it-top-to-bottom demo for students who have never seen a class.
Each PART is meant to be shown and discussed in order. Run the whole file
with:  python3 classes_intro_demo.py

The demo deliberately ends on the same SHAPE as the CityModel class in the
Weapons of Math Destruction simulator, so students can then go read that code.
"""


# ---------------------------------------------------------------------------
# PART 1 — Why bother? The "before" picture.
# ---------------------------------------------------------------------------
# Without classes, keeping related data together is clumsy. If we want to track
# several dogs, the name and energy of each float around in separate variables
# (or parallel lists) that we have to keep lined up by hand.

dog1_name = "Rex"
dog1_energy = 100
dog2_name = "Biscuit"
dog2_energy = 80
# ...this gets unmanageable fast, and nothing ties a dog's data to its actions.


# ---------------------------------------------------------------------------
# PART 2 — The "after" picture: one blueprint that bundles data + behavior.
# ---------------------------------------------------------------------------
class Dog:
    """A blueprint for a dog. Each Dog object has its own name and energy."""

    def __init__(self, name, energy=100):
        # __init__ runs automatically when we create a Dog.
        # 'self' is THIS particular dog. We attach attributes to it.
        self.name = name
        self.energy = energy

    def bark(self):
        # A method: a function that belongs to the object.
        return f"{self.name} says: Woof!"

    def play(self):
        # Methods can read and change the object's own attributes.
        if self.energy <= 0:
            return f"{self.name} is too tired to play."
        self.energy -= 20
        return f"{self.name} plays! Energy is now {self.energy}."


# ---------------------------------------------------------------------------
# PART 3 — Using the blueprint. Each call to Dog(...) makes a new INSTANCE.
# ---------------------------------------------------------------------------
def demo():
    rex = Dog("Rex")              # rex is an instance of Dog
    biscuit = Dog("Biscuit", 60)  # a separate instance with its own data

    print(rex.bark())             # we never pass 'self' — Python does it for us
    print(biscuit.bark())

    print(rex.play())
    print(rex.play())             # rex's energy drops; biscuit's is untouched
    print(f"Meanwhile, {biscuit.name} still has energy {biscuit.energy}.")

    print()
    print("Key point: rex and biscuit are independent objects built from the")
    print("same blueprint. Each carries its own data AND its own behavior.")


if __name__ == "__main__":
    demo()


# ===========================================================================
# BRIDGE TO THE WMD SIMULATOR (talk through, don't run)
# ===========================================================================
# The CityModel class in the predictive-policing demo has the exact same shape:
#
#     class CityModel:
#         def __init__(self):     # sets up the districts (the data)
#             ...
#         def step(self):         # runs one round (the behavior)
#             ...
#
# Once students see that __init__ = "set up the starting data" and a method =
# "an action the object can take," the simulator stops looking like magic and
# starts looking like a Dog that happens to model a city.