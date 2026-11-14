# Roadmap: Self-Driving Car

A 2D top-down car in pygame that learns to drive by evolution. It sees the walls with raycasts and decides with a neural network you write by hand in NumPy.

## End goal (the stop line)

The project is **done** when every box below is ticked. Then we stop. No "one more feature".

- [x] A brain trained by evolution completes a full lap on every training track (5 tracks).
- [x] The same saved brain, with no extra training, completes a full lap on at least 2 of 3 test tracks it has never seen.
- [x] One command trains from scratch, and one command runs a saved brain on any track.
- [x] The README has: what it is, how to run it, a fitness-per-generation plot, a GIF of the car driving an unseen track, a results table (lap completion per track), and an honest "where it fails and why" section.
- [ ] You can explain every part of the code without looking it up.

The "2 of 3" number may change **once**, at M8, if results show it's unrealistic. The reason goes in the README, and then it doesn't move again.

## Rules that keep it finite

- New ideas go in the **Parking lot** at the bottom, never into the current milestone.
- A milestone is done when its "done when" boxes pass, not when it's pretty.
- Milestones go in order. No skipping ahead.
- When the end goal is met, the project is frozen. Parking lot ideas become a new project if you still want them.

## What you'll know at the end

- vectors and trig for movement
- collision detection
- raycasting
- NumPy arrays and matrix math
- a neural network's forward pass, written by hand
- genetic algorithms: selection, elitism, mutation, crossover
- fitness design (the evolution version of reward design)
- overfitting vs generalization, measured properly
- saving models, plotting results, writing up experiments honestly

## Milestones

### M0: Setup

**Goal:** an empty project that runs.
**Research:** virtual environments (`python -m venv`) and why we use them.

Done when:
- [x] git repo and venv created, pygame and numpy installed
- [x] `.gitignore` excludes the venv
- [x] a pygame window opens and closes cleanly
- [x] first commit

### M1: A car you can drive

**Goal:** drive a car with the arrow keys: accelerate, brake, turn.
**Learn:** angles, sin and cos, position and velocity, the game loop.
**Research:** "how sin and cos turn an angle into x and y movement", `pygame.transform.rotate`, "fixed timestep game loop".

Done when:
- [x] the car turns smoothly and its image rotates with it
- [x] it has acceleration, friction and a max speed
- [x] each update moves the car by a fixed step, not by real elapsed time (needed later to train faster than real time)
- [x] you can explain which of sin and cos drives x and which drives y in your setup, and why

### M2: Track and crashes

**Goal:** the car drives on a track and crashes into walls.
**Learn:** loading images, pixel colors, collision detection.
**Research:** `Surface.get_at`, `pygame.mask`, "pixel perfect collision pygame". Tracks are generated images: two flat colors, 800 × 600.

Done when:
- [x] the track is loaded from an image
- [x] touching a wall crashes the car (stops or resets it) every time
- [x] driving on the road never triggers a crash
- [x] the crash check uses the car's corners or shape, not only its center

### M3: Eyes (raycasts)

**Goal:** the car "sees" the walls.
**Learn:** raycasting, normalizing inputs.
**Research:** "2D raycasting", "ray marching vs line intersection", "why normalize neural network inputs".

Done when:
- [x] 5 rays are drawn from the car at fixed angles relative to its heading, and they stop at walls
- [x] each ray returns a distance, capped at a max length
- [x] distances print as numbers from 0 to 1 and match what you see on screen
- [x] the rays turn with the car

### M4: Progress score

**Goal:** measure how far along the track the car got.
**Learn:** designing a fitness score, which is the evolution version of your maze reward.
**Research:** "checkpoints in racing games". Then think: why can't fitness just be "distance driven"?

Done when:
- [x] checkpoints (gates) are placed along the track in order
- [x] the score goes up only when the car passes the next checkpoint in order
- [x] driving backwards or spinning in circles doesn't raise the score
- [x] a full lap is detected
- [x] you can answer the "why not distance driven" question

### M5: A brain (neural network from scratch)

**Goal:** the car drives itself using a neural network you wrote in NumPy. It will drive badly, and that's fine.
**Learn:** matrices, the dot product, weights and biases, activation functions, the forward pass.
**Research:** 3Blue1Brown's "But what is a neural network?", `np.dot` and `@`, `np.tanh`.

Done when:
- [x] the network takes the ray distances as input (plus speed, if you want)
- [x] it outputs steering and throttle
- [x] the weights start random, and the car drives with no keyboard
- [x] you can explain the shape of every weight matrix and why it has that shape

### M6: A population

**Goal:** many cars at once, each with its own brain.
**Learn:** classes, managing many objects, simulation speed.
**Research:** Python classes (`__init__`, methods), "pygame performance with many sprites".

Done when:
- [x] 50 or more cars drive at once
- [x] each car stops when it crashes or hits a time limit
- [x] a generation ends when every car has stopped
- [x] the best fitness of each generation is printed
- [x] drawing can be turned off so training runs faster than real time

### M7: Evolution

**Goal:** cars get better every generation.
**Learn:** genetic algorithms (selection, elitism, mutation, crossover) and their hyperparameters.
**Research:** "genetic algorithm explained", "neuroevolution", "elitism in genetic algorithms".

Done when:
- [x] each new generation is made from the best brains of the last one
- [x] best fitness per generation is saved and plotted with matplotlib, and the line goes up
- [x] a car completes a full lap on your first track
- [x] you can explain what happens when mutation is too big and when it's too small, because you tried both

### M8: Generalization test

**Goal:** prove the car learned to drive, not to memorize one track.
**Learn:** overfitting vs generalization, train/test split, saving models.
**Research:** "overfitting", `np.save` and `np.load`.

Done when:
- [x] 5 training tracks and 3 test tracks are drawn, and the test tracks are never used in training
- [x] training uses all 5 training tracks
- [x] the best brain is saved to a file and loaded back
- [x] evaluation prints lap completion % for every track, with training and test tracks shown separately

### M9: Experiments and write-up

**Goal:** understand why it works and where it breaks.
**Learn:** running fair experiments, reporting results honestly.

Done when:
- [x] 2 or 3 experiments are run, each changing one thing (for example the number of rays, the hidden layer size, or the mutation rate), and the results are recorded
- [x] the README is complete (see the end goal)
- [ ] every end goal box is ticked, and the project is done

## Parking lot (not now)

- DQN with PyTorch on the same game, then race it against the evolution car
- racing against cars built by other AIs, like in the video
- a "surprise" test track with something no training track has (an obstacle, or tighter turns)
- a human vs AI race mode
- a track editor inside the game
- sound, menus, nicer graphics
- realistic physics like drifting or tire grip
