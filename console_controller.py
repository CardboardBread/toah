"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""


# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro
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


from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """
    try:
        model.move(origin, dest)
    except IllegalMoveError as e:
        raise IllegalMoveError(e)

class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
        self._play = True
        self._game = True
        self._model = TOAHModel(number_of_stools)
        self._model.fill_first_stool(number_of_cheeses)
        self._cheeses = number_of_cheeses
        self._stools = number_of_stools

    def print_model(self):
        """Prints the state of the TOAH model to the console.

        @param ConsoleController self:
        @rtype: None 
        """
        print('The model currently looks like this:')
        print(self._model)

    def move_command(self):
        """Procedure for handling when the user wants to move a wheel of cheese

        @param ConsoleController self:
        @rtype: None 
        """
        self._moving = True

        while(self._moving):
            source = input('Please indicate the index of the stool '\
                           'you want to move from, or C to [C]ancel\n')

            if (source == 'C') or (source == 'c'):
                self._moving = False
                break

            try:
                source = int(source)
            except:
                print('Input is not a valid index!')
                continue

            if source >= self._stools:
                print('No stool exists at given index!')
                continue

            break
            
        while(self._moving):
            dest = input('Please indicate the index of the stool '\
                         'you want to move to, or C to [C]ancel\n')

            if (dest == 'C') or (dest == 'c'):
                self._moving = False
                break

            try:
                dest = int(dest)
            except:
                print('Input is not a valid index!')
                continue

            if dest >= self._stools:
                print('No stool exists at given index!')
                continue

            try:
                self._model.move(source, dest)
                self.print_model()
                self._moving = False
                continue
            except IllegalMoveError as ime:
                print(ime)
                self._moving = False
                continue

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None
		
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """

        print("Starting a TOAH with " + \
              str(self._stools) + " number of " \
              "stools and " + str(self._cheeses) + \
              " number of cheeses.")
        print(self._model)
        
        while(self._play):

            self._moving = False
            empty = False

            user = input('Options: [M]ove [Q]uit [R]estart [P]rint\n')
            
            if user:
                if (user == 'M') or (user == 'm'):
                    self.move_command()
                    
                elif (user == 'Q') or (user == 'q'):
                    print('Quitting...')
                    break
                
                elif (user == 'R') or (user == 'r'):
                    print('Restarting...')
                    new_toah = ConsoleController(self._cheeses,self._stools)
                    new_toah.play_loop()
                    break
                
                elif (user == 'P') or (user == 'p'):
                    self.print_model()
                    
                else:
                    continue
            else:
                continue

if __name__ == '__main__':
    toah = ConsoleController(3,3)
    toah.play_loop()
