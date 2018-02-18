"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2018.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "__main__":'

import time
from toah_model import TOAHModel

def get_tops(model):
    """Returns a list of the cheese of on the top of each stool.

    @param TOAHModel model:
    @rtype: list of SomeClass
    """
    out = []
    for i in range(model.get_number_of_stools()):
        if model.get_top_cheese(i) is not None:
            out.append(model.get_top_cheese(i).size)
        else:
            out.append(0)
    return out

def empty_stack(model, cheeses_left, delay, animate):
    """Empty's stacks in the model.

    @param TOAHModel model:
    @param cheeses_left int:
    @param delay int:
    @param animate bool:
    @rtype: None
    """
    while (nonzero(model) < cheeses_left) and (0 in get_tops(model)):
        tops = get_tops(model)
        if max(tops) == tops[-1]:
            model.move(tops.index(max(tops[0:3])), tops.index(0))
            if animate:
                time.sleep(delay)
                print(model)
        else:
            model.move(tops.index(max(tops)), tops.index(0))
            if animate:
                time.sleep(delay)
                print(model)

def nonzero(model):
    """Returns the amount of nonzero tops remaining in the model

    @param TOAHModel model:
    @rtype: int
    """
    nonzero = 0
    for top in get_tops(model)[0:3]:
        if top != 0:
            nonzero += 1
    return nonzero

def condense(model, delay, animate):
    """Performs an ideal condense on the smallest pair available.

    @type model: TOAHModel
    @param delay int:
    @param animate bool:
    @rype: None
    """
    #if min(tops) + 1 in tops and min(tops) != 0:
    #    model.move(tops.index(min(tops)), tops.index(min(tops) + 1))
    tops = get_tops(model)
    ordered = tops[:]
    ordered.sort()
    
    for val in ordered:
        if val + 1 in ordered and val != 0:
            model.move(tops.index(val), tops.index(val + 1))
            if animate:
                time.sleep(delay)
                print(model)
            break

def victory_check(model, cheeses_left, delay, animate):
    """Attempts to victory place, if the model's current state supports it.

    @type model: TOAHModel
    @param cheeses_left int:
    @param delay int:
    @param animate bool:
    @rype: bool
    """
    tops = get_tops(model)

    if tops[-1] == 1:
        return

    if tops[-1] == 0 and max(tops) == 5:
        model.move(tops.index(max(tops)), -1)
        if animate:
            time.sleep(delay)
            print(model)
        return True

    if tops[-1] == cheeses_left + 1 and max(tops[0:3]) == cheeses_left:
        model.move(tops.index(max(tops[0:3])), -1)
        if animate:
            time.sleep(delay)
            print(model)
        return True

    return False
            
def victory_state(model):
    """For checking if the model is completed, returns a tops list showing all
    cheeses on the target(right-most) stool.

    @param TOAHModel model:
    @rtype List[int]
    """
    vict = []
    for i in range(model.get_number_of_stools()):
        vict.append(0)
    vict[-1] = 1
    return vict

def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    
    """
    cheeses_left = model.get_number_of_cheeses()
    if model.get_number_of_stools() != 4:
        print('Model does not have four stools!')
        return

    if False: # hand-made solve
        model.move(0, 1) # empty
        model.move(0, 2) # empty
        model.move(0, 3) # empty
        model.move(1, 2) # ideal condense
        model.move(0, 1) # empty
        model.move(3, 1) # ideal condense
        model.move(0, 3) # victory place
        model.move(1, 0) # exposing
        model.move(1, 3) # victory place
        model.move(0, 3) # victory place
        model.move(2, 1) # expose
        model.move(2, 3) # victory place
        model.move(1, 3) # victory place

    while(victory_state(model) != get_tops(model)):
        empty_stack(model, cheeses_left, delay_btw_moves, animate)
        while(victory_check(model, cheeses_left, delay_btw_moves, animate)):
            cheeses_left -= 1
        condense(model, delay_btw_moves, animate)
        while(victory_check(model, cheeses_left, delay_btw_moves, animate)):
            cheeses_left -= 1
            
    # empty as much possible (exposing the largest cheese possible)
    # only ideal condensing 1 -> 2 or 2 -> 3 but not 1 -> 3
    # empty more
    # ideal condense
    # victory place (lowest to target)
    # expose largest not in victory
    # victory place x2
    # expose largest
    # victory place x2

    # empty
    # condense
    # victory check (fail)
    # empty
    # condense
    # victory check (good)

    # remember, we dont expose and condense, that by definition isnt
    # an ideal condense

    # we only need to look at the top of each stack to work
    # since all restacking is ideal

    # expose as much
    # condense the small ones if we cant expose
    # expose
    # always check for victory place
    # expose, condense smallest
    
if __name__ == '__main__':
    num_cheeses = 5
    delay_between_moves = 0.5
    console_animate = True
    time.sleep(delay_between_moves)
    
    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)

    print(four_stools.number_of_moves())
