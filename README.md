# PCGML-Minecraft
This project is my first deep dive into the world of PCG and my attempts at replicating classical machine learning methods in Minecraft.
My code is written in python as this was the easier language to quickly write scripts in when doing this project. One other option
would have been to use java because Minecraft runs using java, but there are less resources and machine learning libraries available in java
for if I was to increase the complexity of the project to use more advanced machine learning techniques.

## Considerations
- In order to view the results of an output you will need a copy of Minecraft: Java Edition
- This project assumes using Minecraft 1.19.2 which is crucial to be able to paste the schematics
- To paste the output `.schem` files into Minecraft you will need the mod called `WorldEdit`
  - See https://www.curseforge.com/minecraft/mc-mods/worldedit for how to use this mod and view schematics
## Alternative To WorldEdit
Note that both of these alternatives convert the `.schem` files to `.schematic` files which will cause some data loss
due to `.schematic` being a much older file format. The full representation of the generated schematics should
be viewed with a real copy of Minecraft: Java Edition.
### SketchFab
1. Use https://puregero.github.io/SchemToSchematic/ to convert `.schem` files to `.schematic` files
2. Import these `.schematic` files into `MineWays`: https://www.realtimerendering.com/erich/minecraft/public/mineways/
3. Export the `Mineways` object to `Sketchfab` to view the schematic as a 3d Model 

An example of viewing on `Sketchfab` can be found here: 

https://sketchfab.com/3d-models/test3dschematic-7b8a33280baa477d8a61041c3e2bb3c4
### Online
1. Use https://puregero.github.io/SchemToSchematic/ to convert `.schem` files to `.schematic` files
2. Drag these `.schematic` files into `CubicalXYZ`: https://cubical.xyz/
3. View the schematic in 3D

## Dependencies
- numpy
- schempy (included in this repository)
### For Neural Network Barebones Approach
- Pytorch
- torchvision
- cuda toolkit (if using GPU)

## How to train
There are a number of probabilities already packaged in this repository, though you are free to train your own and use your own input data too!
#### Pre-Requisites
- A set of `.schem` files to use as training data
#### Training
1. Make sure to uncomment the training line in the `main.py` file
2. Run `python main.py` making sure that the path to your input training schematics and the output name of the probabilities `.pickle` file is set.
3. The probabilities will be saved in the `markov/probabilities` folder with the name you gave
4. If you left the generation line uncommented, then the probabilities will be used to generate a single new schematic
5. The schematic will be saved in the `output` folder with the name you gave as parameter to the `generate` function

## How to generate
There are a number of probabilities already packaged in this repository, though you are free to train your own and use your own input data too!
#### Pre-Requisites
- At least one probability `.pickle` file that the generation script can use to generate a new schematic
- If using version `3` or version `4` then you will need to have 2 probabilities trained from the same versions of training scripts
#### Generation
1. Make sure to uncomment the generation line in the `main.py` file
2. If you dont want to also train new probabilities, then make sure to comment out the training line
3. Run `python main.py` making sure that the path to your input probabilities and the output name of the generated schematic `.schem` file is set.
4. The input probabilities is just the name that you gave the probabilities file when you trained it, not the entire path
5. In version `4` you can optionally pass a tuple of size to the generate function to specify the size of the output schematic for example: (50, 50, 50)
6. The schematic will be saved in the `output_schems` folder with the name you gave as parameter to the `generate` function

## **Follow instructions in the `Considerations` section to view the output schematics**
