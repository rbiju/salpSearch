# Simulating food finding behavior in Salps

Salps are ocean creatures that are widely believed to be the most efficient example of jet propulsion in the animal kingdom. They are not very bright,
yet they participate in chaining behavior that makes them uncanny at finding areas with high concentrations of food. I am seeking to determine if I can 
reproduce this 'concentration gradient ascent' with a simple rule for each salp to follow.

A simulation was coded in python using the pymunk physics engine to compute chain behavior and the pygame module to render the results in real time.
To run the simulation, simply install the required modules:
pygame,
pymunk,
numnpy,
numba (optional, but highly recommended for an FPS above 0.1).

Then, run salpSim.py, changing the FPS in the object call in the last line to suit your computer's capabilities.

Future plans include new salp chain shapes, GUI interface for some hyperparameters, and parameter optmization with a genetic algorithm
