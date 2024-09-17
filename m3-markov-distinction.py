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

STITCHES = ["sc", "dc", "tc"] # acronyms for single crochet, double crochet, triple crochet

class MarkovCrochet:
    def __init__(self, stitches, colours, yarn_weight, size):
        self.stitches = stitches.copy()
        self.stitches.append("tch") # turning chain signifies new row
        self.colours = colours
        if len(self.colours) > 1:
            self.stitches.append("chc") # include change colour step if multiple colours
        if yarn_weight == 'random':
            self.yarn_weight = np.random.choice(
                list(YARN_GAUGES.keys()), 
                p=[1/len(YARN_GAUGES.keys()) for i in range(0, len(YARN_GAUGES.keys()))])
        else:
            self.yarn_weight = yarn_weight
        self.length = 0
        if size == 'random':
            self.length = np.random.randint(1, 15)
        else:
            self.length = SIZES[size]

        self.transition_matrix = {}

        for stitch in self.stitches:
            prob_distribution = {}
            random_vals = np.random.rand(len(self.stitches))
            probs = random_vals / sum(random_vals)
            for i in range(0, len(self.stitches)):
                next_stitch = self.stitches[i]
                prob = probs[i]
                prob_distribution[next_stitch] = prob
            
            self.transition_matrix[stitch] = prob_distribution
    
    def get_new_stitch(self, curr_stitch):
        next_stitch = np.random.choice(
            self.stitches,
            p = list(self.transition_matrix[curr_stitch].values())
        )
        return next_stitch

    
    def make_pattern(self, start_stitch, start_colour):
        stitch_len = YARN_GAUGES[self.yarn_weight]
        curr_len = 0
        curr_colour = start_colour
        curr_stitch = start_stitch
        pattern = []

        while curr_len < self.length:
            curr_row = []

            """
            keep building this row until turning chain, or until it reaches 20 stitches 
            so that it's not too long for visualization
            """
            while curr_stitch != "tch" and len(curr_row) < 10: 
                if curr_stitch == "chc":
                    random_vals = np.random.rand(len(self.colours))
                    probs = random_vals / sum(random_vals)
                    new_colour = curr_colour
                    while new_colour == curr_colour: # to prevent the current colour from being picked again
                        new_colour = np.random.choice(self.colours, p=probs)
                    curr_colour = new_colour
                else:
                    curr_row.append((curr_stitch, curr_colour))
                next_stitch = self.get_new_stitch(curr_stitch)
                curr_stitch = next_stitch

            if len(curr_row) > 0: # in case first stitch of row is turning chain
                pattern.append(curr_row)
                curr_len = curr_len + stitch_len

            curr_stitch = self.get_new_stitch("tch")
        
        self.length = curr_len
        
        return pattern
    

class PatternVisualizer:
    def __init__(self, master = None):
        self.master = master
        self.canvas = Canvas(self.master)

    def draw_stitch(self, x1, y1, x2, y2, colour):
        self.canvas.create_arc(x1, y1, x2, y2, start=120, extent=300, 
                               outline=colour, fill=colour, width=2)
     
    def draw_pattern(self, pattern):
        x1 = 250
        y1 = 70
        x2 = 280
        y2 = 140
        width = x2 - x1
        height = y2 - y1
         
        for i in range(0, len(pattern)):
            curr_row = pattern[i]

            for idx in range(0, len(curr_row)):
                elem = curr_row[idx]
                stitch = elem[0]
                colour = elem[1]

                # print(f"Stitch {idx} of row {i}")
                # print(f"x1: {x1}, x2: {x2}")

                match stitch:
                    case "sc":
                        self.draw_stitch(x1, y1, x2, y2, colour)
                        self.canvas.create_oval(x1-8, y1, x2+8, y1+10, outline=colour, fill=colour, width=2)
                        self.canvas.create_oval(x1-8, y2, x2+8, y2+10, outline=colour, fill=colour, width=2)
                    case "dc":
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
                
                if idx == len(curr_row) - 1:
                    # print(f"Last row! Stitch {idx} of row {i}")
                    continue
                elif i % 2 == 0: # if index is even, it is an odd row and thus going from left to right 
                    x1 = x1 + width
                    x2 = x2 + width
                else: # if index is odd, it is an even row
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
    while not stitches_done:
        stitch_input = input()
        if stitch_input == "done":
            stitches_done = True
        elif stitch_input not in STITCHES:
            print("Invalid stitch. Try again.\n")
        else:
            if stitch_input not in stitches:
                stitches.append(stitch_input.lower())
    print("\n")
    
    print(f"What colours would you like to use? Type 'done' when you have finished adding.\n")
    colours = []
    colours_done = False
    while not colours_done:
        colour_input = input()
        if colour_input == "done":
            colours_done = True
        else:
            if colour_input not in colours:
                colours.append(colour_input.lower())
    print("\n")

    print("Okay! Generating pattern now...\n")

    pattern_maker = MarkovCrochet(stitches, colours, yarn_weight, size)

    start_stitch = np.random.choice(
        pattern_maker.stitches, 
        p=[1/len(pattern_maker.stitches) for i in range(0, len(pattern_maker.stitches))])
    start_colour = np.random.choice(
        pattern_maker.colours, 
        p=[1/len(pattern_maker.colours) for i in range(0, len(pattern_maker.colours))])

    pattern = pattern_maker.make_pattern(start_stitch, start_colour)

    print(f"Yarn weight: {pattern_maker.yarn_weight}\n")
    print(f"Length: {pattern_maker.length}cm\n")
    print(f"Stitches used: {stitches}\n")
    print(f"Colours used: {colours}\n")

    for num in range(0, len(pattern)):
        row = pattern[num]
        stitches = []
        for stitch in row:
            stitches.append(f"{stitch[0]} ({stitch[1]})")
        str = ', '.join(stitches)
        if num % 2 == 0:
            print(f"Row {num} (l-->r): {str}")
        else:
            print(f"Row {num} (r-->l): {str}")


    master = Tk()
    visualizer = PatternVisualizer(master)
    
    visualizer.draw_pattern(pattern)

    # Sets the geometry and position
    # of window on the screen
    master.geometry("800x1000+350+0")
 
    # Infinite loop breaks only by interrupt
    mainloop()


if __name__ == "__main__":
    main()