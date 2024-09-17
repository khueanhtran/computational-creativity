"""
Markov Crochet Pattern Generator:

Generates and visualizes new crochet patterns based on some user inputs 
and a Markov chain with randomized probability distributions.

Author: Khue Anh Tran
"""

import numpy as np
from tkinter import * 
from tkinter.ttk import * 

YARN_GAUGES = {
    "bulky" : 3,
    "medium" : 2,
    "fine" : 1
} # length of one stitch for each type of yarn weight; unit = cm

SIZES = {
    "s" : 5,
    "m" : 10, 
    "l" : 15
} # estimated length in cm for sizes small, medium, and large

STITCHES = ["sc", "dc", "tc"] # standard acronyms for single crochet, double crochet, triple crochet

class MarkovCrochet:
    """
    Crochet pattern generator using a first-order Markov chain
    """
    def __init__(self, stitches, colours, yarn_weight, size):
        self.stitches = stitches.copy()
        self.stitches.append("tch") # turning chain signifies new row

        self.colours = colours
        if len(self.colours) > 1:
            self.stitches.append("chc") # include change colour option if multiple colours

        if yarn_weight == 'random':
            # choose random yarn weight from uniform probability distribution
            self.yarn_weight = np.random.choice(
                list(YARN_GAUGES.keys()), 
                p=[1/len(YARN_GAUGES.keys()) for i in range(0, len(YARN_GAUGES.keys()))])
        else:
            self.yarn_weight = yarn_weight

        self.length = 0
        if size == 'random':
            # choose random length with size l as the upper limit
            self.length = np.random.randint(1, 15)
        else:
            self.length = SIZES[size]

        self.transition_matrix = {}

        # generate randomized transition matrix
        for stitch in self.stitches:
            prob_distribution = {}
            random_vals = np.random.rand(len(self.stitches)) # randomize value for each type of stitch
            probs = random_vals / sum(random_vals) # normalize values so they sum to 1
            # assign probability to each possible next stitch
            for i in range(0, len(self.stitches)):
                next_stitch = self.stitches[i]
                prob = probs[i]
                prob_distribution[next_stitch] = prob
            
            self.transition_matrix[stitch] = prob_distribution
    
    def get_new_stitch(self, curr_stitch):
        """
        Chooses a next stitch based on the probability distrbution associated
        with the current stitch
        """
        next_stitch = np.random.choice(
            self.stitches,
            p = list(self.transition_matrix[curr_stitch].values())
        )
        return next_stitch

    
    def make_pattern(self, start_stitch, start_colour):
        """
        Creates entire pattern using transition matrix and starting stitch and colour
        """
        stitch_len = YARN_GAUGES[self.yarn_weight]
        curr_len = 0 # keep track of growing length of piece
        curr_colour = start_colour
        curr_stitch = start_stitch
        pattern = [] # 2D list to represent pattern

        # keep building pattern until desired length is reached
        while curr_len < self.length:
            curr_row = [] # list to represent a row

            
            # keep building this row until turning chain, or until it reaches 15 stitches 
            # so that it's not too long for visualization
            while curr_stitch != "tch" and len(curr_row) < 15: 
                if curr_stitch == "chc": # if change colour
                    # choose random values for each colour
                    random_vals = np.random.rand(len(self.colours))
                    probs = random_vals / sum(random_vals) # normalize values
                    new_colour = curr_colour
                    while new_colour == curr_colour: # to prevent the current colour from being picked again
                        # choose random colour based on randomized probability distribution
                        new_colour = np.random.choice(self.colours, p=probs)
                    curr_colour = new_colour
                else: # any other stitch/option
                    curr_row.append((curr_stitch, curr_colour))

                next_stitch = self.get_new_stitch(curr_stitch) # get next stitch
                curr_stitch = next_stitch

            if len(curr_row) > 0: # unless first stitch of row is turning chain/row is empty
                pattern.append(curr_row)
                curr_len = curr_len + stitch_len

            curr_stitch = self.get_new_stitch("tch") # generate first stitch for new row
        
        self.length = curr_len # for later display
        
        return pattern
    

class PatternVisualizer:
    """
    Draws out a given pattern in a new pop-up window
    """
    def __init__(self, master = None):
        self.master = master
        self.canvas = Canvas(self.master)

    def draw_stitch(self, x1, y1, x2, y2, colour):
        """
        Draws one stitch (without the top and bottom) 
        given positioning coordinates and colour
        """
        self.canvas.create_arc(x1, y1, x2, y2, start=120, extent=300, 
                               outline=colour, fill=colour, width=2)
     
    def draw_pattern(self, pattern):
        """
        Draws the shapes for the stitches of a given pattern
        """
        # starting coordinates
        x1 = 250
        y1 = 40
        x2 = 280
        y2 = 110
        width = x2 - x1
        height = y2 - y1
         
        # loop through the entire pattern, row by row
        for i in range(0, len(pattern)):
            curr_row = pattern[i]

            # loop through a row, stitch by stitch
            for idx in range(0, len(curr_row)):
                elem = curr_row[idx]
                stitch = elem[0]
                colour = elem[1]

                # drawing is different for each type of stitch
                match stitch:
                    case "sc": # single crochet
                        self.draw_stitch(x1, y1, x2, y2, colour)
                        # ovals for the top and bottom of each stitch
                        self.canvas.create_oval(x1-8, y1, x2+8, y1+10, outline=colour, fill=colour, width=2)
                        self.canvas.create_oval(x1-8, y2, x2+8, y2+10, outline=colour, fill=colour, width=2)
                    case "dc": # double crochet
                        y11 = y1 + 5
                        y21 = y11 + round(height/2)
                        y12 = y21 - 5
                        y22 = y2
                        self.draw_stitch(x1, y11, x2, y21, colour)
                        self.draw_stitch(x1, y12, x2, y22, colour)
                        self.canvas.create_oval(x1-8, y1, x2+8, y1+10, outline=colour, fill=colour, width=2)
                        self.canvas.create_oval(x1-8, y2, x2+8, y2+10, outline=colour, fill=colour, width=2)
                    case "tc":
                        y11 = y1 + 7
                        y21 = y11 + round(height/3)
                        y12 = y21 - 5
                        y22 = y12 + round(height/3)
                        y13 = y22 - 5
                        y23 = y2
                        self.draw_stitch(x1, y11, x2, y21, colour)
                        self.draw_stitch(x1, y12, x2, y22, colour)
                        self.draw_stitch(x1, y13, x2, y23, colour)
                        self.canvas.create_oval(x1-8, y1, x2+8, y1+10, outline=colour, fill=colour, width=2)
                        self.canvas.create_oval(x1-8, y2, x2+8, y2+10, outline=colour, fill=colour, width=2)
                
                
                if idx == len(curr_row) - 1: # don't update x-coordinates if going to new row
                    continue # first stitch of new row needs to align vertically of last stitch of previous row
                elif i % 2 == 0: # if index is even, it is an odd row and thus going from left to right 
                    x1 = x1 + width
                    x2 = x2 + width
                else: # if index is odd, it is an even row and thus going from right to left
                    x1 = x1 - width
                    x2 = x2 - width
            
            # moving down to a new row
            y1 = y1 + height
            y2 = y2 + height
         
        self.canvas.pack(fill = BOTH, expand = 1)


def main():
    print("Welcome to Creative Crochet Pattern Generator!\n")

    weight_options = list(YARN_GAUGES.keys())
    weight_options.append("random") # option to randomize yarn weight
    print(f"What type of yarn are you using? {weight_options}\n")
    yarn_weight = input()
    print("\n")

    size_options = list(SIZES.keys())
    size_options.append("random") # option to randomize size
    print(f"What size are you thinking? {size_options}\n")
    size = input()
    print("\n")

    print(f"What stitches would you like to use? Type 'done' when you have finished selecting.")
    print("'sc' for single crochet")
    print("'dc' for double crochet")
    print("'tc' for triple crochet\n")
    stitches = []
    stitches_done = False
    while not stitches_done: # keep getting input until user signifies completion
        stitch_input = input()
        if stitch_input == "done":
            stitches_done = True
        elif stitch_input not in STITCHES:
            print("Invalid stitch. Try again.\n") # error message
        else:
            if stitch_input not in stitches: # to avoid repeats
                stitches.append(stitch_input.lower())
    print("\n")
    
    print(f"What colours would you like to use? Type 'done' when you have finished adding.\n")
    colours = []
    colours_done = False
    while not colours_done: # keep getting inputs until user signifies completion
        colour_input = input()
        if colour_input == "done":
            colours_done = True
        else:
            if colour_input not in colours: # to avoid repeats
                colours.append(colour_input.lower())
    print("\n")

    print("Okay! Generating pattern now...\n")

    # create new pattern maker
    pattern_maker = MarkovCrochet(stitches, colours, yarn_weight, size)

    # randomly select start stitch with uniform probability distribution
    start_stitch = np.random.choice(
        pattern_maker.stitches, 
        p=[1/len(pattern_maker.stitches) for i in range(0, len(pattern_maker.stitches))])
    # randomly select start colour with uniform probability distribution
    start_colour = np.random.choice(
        pattern_maker.colours, 
        p=[1/len(pattern_maker.colours) for i in range(0, len(pattern_maker.colours))])

    # generate pattern
    pattern = pattern_maker.make_pattern(start_stitch, start_colour)

    print(f"Yarn weight: {pattern_maker.yarn_weight}\n")
    print(f"Length: {pattern_maker.length}cm\n")
    print(f"Stitches used: {stitches}\n")
    print(f"Colours used: {colours}\n")

    # display written pattern
    for num in range(0, len(pattern)):
        row = pattern[num]
        stitches = []
        for stitch in row:
            stitches.append(f"{stitch[0]} ({stitch[1]})")
        str = ', '.join(stitches)
        if num % 2 == 0:
            print(f"Row {num+1} (l-->r): {str}")
        else:
            print(f"Row {num+1} (r-->l): {str}")


    # visualizing pattern

    window = Tk() # start new window for display
    visualizer = PatternVisualizer(window) # visualizations will appear on the created window
    visualizer.draw_pattern(pattern)
    window.title("Generated Crochet Pattern")
    window.geometry("800x1500+350+0") # setting dimensions and positioning on screen for window
 
    mainloop() # window keeps displaying until program is stopped


if __name__ == "__main__":
    main()