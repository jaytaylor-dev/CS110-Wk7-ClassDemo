"""
Intro to Classes — a live-coding demo
=====================================
A short, run-it-top-to-bottom demo for students who have never seen a class.
Each PART is meant to be shown and discussed in order. Run the whole file
with:  python3 classes_intro_demo.py

The demo deliberately ends on the same SHAPE as the CityModel class in the
Weapons of Math Destruction simulator, so students can then go read that code.

This version lets STUDENTS build the dogs by typing input, then stores every
dog in a list and prints them all back out at the end.
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
# It's even worse if we don't know up front HOW MANY dogs there will be —
# which is exactly the case when we let a user type them in (see PART 4).


# ---------------------------------------------------------------------------
# PART 2 — The "after" picture: one blueprint that bundles data + behavior.
# ---------------------------------------------------------------------------
class Dog:
    """A blueprint for a dog. Each Dog object has its own name and energy."""

    def __init__(self, name, breed, energy=100):
        # __init__ runs automatically when we create a Dog.
        # 'self' is THIS particular dog. We attach attributes to it.
        self.name = name
        self.breed = breed
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

    def rest(self):
        # The opposite of play(): this method RESTORES the object's energy,
        # capped at 100 so a dog can't rest its way past full.
        self.energy = min(100, self.energy + 30)
        return f"{self.name} rests. Energy is now {self.energy}."

    def describe(self):
        # A method that summarizes this dog — handy for printing later.
        return f"{self.name} is a {self.breed} with energy {self.energy}."


# ---------------------------------------------------------------------------
# PART 3 — Using the blueprint. Each call to Dog(...) makes a new INSTANCE.
# ---------------------------------------------------------------------------
def demo():
    rex = Dog("Rex", "Labrador")            # rex is an instance of Dog
    biscuit = Dog("Biscuit", "Beagle", 60)  # a separate instance, its own data

    print(rex.bark())             # we never pass 'self' — Python does it for us
    print(biscuit.bark())
    print(rex.play())
    print(rex.play())             # rex's energy drops; biscuit's is untouched
    print(f"Meanwhile, {biscuit.name} still has energy {biscuit.energy}.")
    print()
    print("Key point: rex and biscuit are independent objects built from the")
    print("same blueprint. Each carries its own data AND its own behavior.")


# ---------------------------------------------------------------------------
# PART 4 — Now let the USER build the dogs, and store them in a list.
# ---------------------------------------------------------------------------
# This is the payoff of PART 1's complaint: we don't know ahead of time how
# many dogs there are or what they'll be called. A class + a list handles any
# number of them cleanly. Each Dog the user describes becomes its own object,
# and we keep them together in one list called `kennel`.
def build_dogs_from_input():
    kennel = []  # an empty list that will hold every Dog object we create

    print("\nLet's build some dogs! (Press Enter for the name when you're done.)")
    while True:
        name = input("\nDog's name: ").strip()
        if name == "":
            break  # blank name signals "no more dogs"

        breed = input("Breed: ").strip() or "mixed breed"

        # input() always returns a string, so we convert energy to an int.
        # We guard against bad input so a typo doesn't crash the demo.
        energy_text = input("Starting energy (just press Enter for 100): ").strip()
        if energy_text == "":
            energy = 100
        elif energy_text.isdigit():
            energy = int(energy_text)
        else:
            print("  (That wasn't a number — defaulting to 100.)")
            energy = 100

        # Build the object from the user's input and store it in the list.
        new_dog = Dog(name, breed, energy)
        kennel.append(new_dog)
        print(f"  Created: {new_dog.describe()}")

    return kennel


# ---------------------------------------------------------------------------
# PART 5 — Retrieve the dogs back out of the list and print each one.
# ---------------------------------------------------------------------------
def print_all_dogs(kennel):
    print("\n" + "=" * 50)
    if not kennel:
        print("No dogs were created.")
        return

    print(f"You created {len(kennel)} dog(s). Here they all are:\n")
    # Loop over the list to RETRIEVE each Dog object we stored earlier.
    # enumerate() just gives us a counter (1, 2, 3, ...) alongside each dog.
    for number, dog in enumerate(kennel, start=1):
        print(f"{number}. {dog.describe()}")
        print(f"   {dog.bark()}")

    # Bonus: group them by breed to print "each TYPE of dog" we created.
    print("\nBreeds in the kennel:")
    breeds = {}
    for dog in kennel:
        breeds[dog.breed] = breeds.get(dog.breed, 0) + 1
    for breed, count in breeds.items():
        print(f"  {breed}: {count}")


# ---------------------------------------------------------------------------
# PART 6 — Interact with the stored dogs: bark, play, rest.
# ---------------------------------------------------------------------------
# Now that every Dog lives in the `kennel` list, we can pull individual ones
# back out and call their methods. The user types a dog's NAME; we search the
# list for the matching object, then run the action they pick. Watch how
# play() and rest() change THAT dog's energy while leaving the others alone.
def find_dog(kennel, name):
    # Retrieve one Dog object out of the list by matching its name.
    # (Case-insensitive so "rex" finds "Rex".)
    for dog in kennel:
        if dog.name.lower() == name.lower():
            return dog
    return None  # no dog by that name


def interact_with_dogs(kennel):
    if not kennel:
        return  # nothing to interact with

    print("\n" + "=" * 50)
    print("Now let's play with the dogs!")
    print("Type a dog's name to pick it, or press Enter to quit.")

    while True:
        name = input("\nWhich dog? (Enter to quit): ").strip()
        if name == "":
            print("All done. Goodbye!")
            break

        dog = find_dog(kennel, name)
        if dog is None:
            # Remind the user which names exist, so typos are easy to fix.
            available = ", ".join(d.name for d in kennel)
            print(f"  No dog named '{name}'. Try one of: {available}")
            continue

        action = input("  Action — (b)ark, (p)lay, (r)est: ").strip().lower()
        if action in ("b", "bark"):
            print("  " + dog.bark())
        elif action in ("p", "play"):
            print("  " + dog.play())
        elif action in ("r", "rest"):
            print("  " + dog.rest())
        else:
            print("  Not an action — type b, p, or r.")


if __name__ == "__main__":
    demo()                              # PARTS 1-3: the scripted blueprint demo
    my_dogs = build_dogs_from_input()   # PART 4: user types dogs into existence
    print_all_dogs(my_dogs)             # PART 5: retrieve + print them all
    interact_with_dogs(my_dogs)         # PART 6: bark / play / rest each dog


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
#
# The list-of-objects idea from PART 4-5 also carries over: anywhere a program
# needs to manage MANY of the same kind of thing (dogs, districts, students,
# loan applicants...), the pattern is the same — one class as the blueprint,
# one list to hold the instances, and a loop to work through them.