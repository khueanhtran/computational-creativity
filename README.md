# Markov Crochet Pattern Generator

This program simulates a creative generator for simple crochet patterns. It asks the user for certain inputs (e.g. type of yarn, size, colours), then generates a basic pattern for the user to follow. The program also visualizes what the crochet piece based on the pattern would look like. 

The pattern generator is built on a first-order Markov chain in which the next stitch is determined based on a randomized probability distrbution that is associated with the current stitch. When the generator is prompted to change colours, which colour comes next is also determined based on randomized probability distributions. 

The pattern visualizer uses `tkinter`, a Python interface for creating Graphical User Interfaces (GUIs). The `Canvas` class is specifically employed to draw shapes that imitate the look of a work of crochet.


## Installation

Download Python at https://www.python.org/downloads/.

Install `numpy` using `pip`:
``` bash
pip install numpy
```

Download the Python file `m3-markov-distinction.py`.


## Usage

To run the program, simply run the Python file either in an IDE or in a terminal window. The program will begin to prompt some inputs from the user - follow the instructions that the program gives. The generated pattern will be displayed in the terminal, while an additional window will pop up for the visualization of the pattern. 


## Personal Connection

This program is inspired by my hobby of crocheting. It is something I picked up when I first started college and have since kept up with somewhat consistently. I really enjoy it as a craft activity that allows me to engage my motor skills and creativity, all while producing items that I can actually use in my life. However, when I crochet, I often follow patterns and only make small creative liberties in terms of colour or minor deviations/changes. I do not usually crochet free-hand or create new patterns for myself, since the design element can be rather difficult. Thus, I was interested in the idea of using **computational creativity** to generate patterns that can inspire out-of-the-box designs for crochet projects. Since the generator does not necessarily make patterns for specific items (e.g. scarf, sweater, hat), there is more novelty involved in the patterns that it comes up with. 

Moreover, I find that with crocheting (at least when compared to knitting, which is a different way of working with yarn that I also do), there is actually a lot of flexibility to take up creative liberties in what you make. This flexibility is not only reflected in the randomization of the pattern generator but also accommodated for, as it makes the patterns that are created by the generator more likely to be replicable. Additionally, for the M1 module of our class, I asked my friend Luna (who actually taught me how to crochet) about the computationally creative system that she would like to make, and she responded with a system that makes new crochet or knitting patterns. I thought this program was a good opportunity to partially explore what this could potentially look like.


## Challenges

In creating this program, I had to take into account how crocheting works to translate into the way that the generator makes its patterns. While the patterns are very simplified and not completely realisitic, there are things in the code that reflect the actual workings of crochet; for example, when you start a new row in crochet, you turn your work and start working in the opposite direction, which is seen in the way the visualizer changes direction when drawing stitches for a new row. Another detail is the idea of yarn gauges, which often refers to the length that a certain number of stitches with a certain type of yarn would yield. I took this idea and simplified it by ascribing one stitch of a certain yarn weight to a specific length. This affects the number of rows that the generator would yield, as a bulkier yarn would achieve a certain length with less rows than a finer yarn, which is how it would be in real life.

Moreover, a big learning opportunity for me with this program was the visualization aspect. I had to start by researching what type of visualizer would suit my needs for the program. I initially thought about using images to represent the stitches, but quickly realized it would be more difficult to apply different colours to the images, and there also are not images out there of singular stitches of different kinds. I pivoted to drawing out my stitches, and landed on `tkinter` for this. I had never used `tkinter` before, so I had to learn how to draw shapes and position them using this interface. It was also quite a challenge to simulate the way the crochet looks by drawing shapes, but I did my best with the tools offered by `tkinter`.

I have not had too much experience with independent coding for entire programs without a lot of guidance on what to create or how to approach things. These challenges are therefore valuable for me to figure out these aspects by myself and allow myself to not feel as overwhelmed by big and open programming projects.

Going forward, I would like to incorporate real-world knowledge about how certain things work even more into my programs, in the hopes of increasing the complexity of the programs and making them more realistic. I would like to continue learning new tools that I have not used before. Additionally, I would like to push for my programs to be as complex as reasonably possible and challenge myself to consider multiple aspects, special cases, details, additions, etc. when coding. 


## Sources

I mainly used this GeeksforGeeks article to learn how to draw shapes with `tkinter`: https://www.geeksforgeeks.org/python-tkinter-create-different-shapes-using-canvas-class/.
