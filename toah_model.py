"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return a MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Ritu Chaturvedi, Samar Sabie
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
#


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
        @param int number_of_stools:
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(number_of_cheeses=5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self._stools = []
        # you must have _move_seq as well as any other attributes you choose
        self._move_seq = MoveSequence([])

        for stool_ind in range(number_of_stools):
            self._stools.append([])

    def get_move_seq(self):
        """ Return the move sequence

        @type self: TOAHModel
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent to the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(number_of_cheeses=7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(number_of_cheeses=7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """
        return self._stools == other._stools

    def _cheese_at(self, stool_index, stool_height):
        """ Return (stool_height)th from stool_index stool, if possible.
        
        @type self: TOAHModel
        @type stool_index: int
        @type stool_height: int
        @rtype: Cheese | None
        
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(number_of_cheeses=5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str

        # This is hard to test
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def get_number_of_cheeses(self):
        """
        Returns the number of cheeses in play in this model.

        @param TOAHModel self:
        @rtype: int

        >>> m = TOAHModel(4)
        >>> m.fill_first_stool(number_of_cheeses=7)
        >>> m.get_number_of_cheeses()
        7
        """
        num = 0
        for stool in self._stools:
            num += len(stool)
        return num

    def get_number_of_stools(self):
        """
        Returns the number of stools in the model.

        @param TOAHModel self:
        @rype: int

        >>> m = TOAHModel(4)
        >>> m.get_number_of_stools()
        4
        """
        return len(self._stools)

    def get_cheese_location(self, cheese):
        """
        Returns the index of the stool on which the given cheese is placed.

        @param TOAHModel self:
        @param Cheese cheese:
        @rtype: int

        >>> m = TOAHModel(4)
        >>> c = Cheese(3)
        >>> m.add(c, 0)
        >>> m.move(0, 1)
        >>> m.get_cheese_location(c)
        1
        """
        for stool in self._stools:
            for fcheese in stool:
                if fcheese.size == cheese.size:
                    return self._stools.index(stool)

    def get_top_cheese(self, stool_index):
        """
        Returns the cheese at the top of the stool at the given index,
        or none if the stool is empty.

        @param TOAHModel self:
        @param stool_index int:
        @rtype: Cheese | None

        >>> m = TOAHModel(4)
        >>> m.get_top_cheese(0)
        """
        if not self._stools[stool_index]:
            return None
        else:
            return self._stools[stool_index][-1]
        

    def move(self, from_stool, stool_index):
        """
        Moves any available cheese from the stool at index 'from_stool',
        onto the stool at index 'stool_index'

        @param TOAHModel self:
        @param from_stool int:
        @param stool_index int:
        @rtype: None

        >>> m = TOAHModel(4)
        >>> m.fill_first_stool()
        >>> m.move(0, 1)
        """
        if self._stools[from_stool]:
            if self._stools[stool_index]:
                if self._stools[stool_index][-1].size < \
                   self._stools[from_stool][-1].size:
                    raise IllegalMoveError('Destination stool has a smaller' \
                                           ' cheese wheel!')
                else:
                    self._stools[stool_index].append( \
                        self._stools[from_stool].pop())
                    self._move_seq.add_move(from_stool, stool_index)
            else:
                self._stools[stool_index].append(self._stools[from_stool].pop())
                self._move_seq.add_move(from_stool, stool_index)
        else:
            raise IllegalMoveError('Move order invalid, source stool is empty!')

    def number_of_moves(self):
        """
        Returns the number of moves that the model has made.

        @param TOAHModel self:
        @rtype: int
        >>> m = TOAHModel(4)
        >>> m.fill_first_stool()
        >>> m.move(0, 1)
        >>> m.move(1, 0)
        >>> m.number_of_moves()
        2
        """
        return self._move_seq.length()

    def add(self, cheese, index):
        """
        Places a new wheel of cheese onto the stool at the given index.

        @param TOAHModel self:
        @param Cheese cheese:
        @param index int:
        @rype: None

        >>> m = TOAHModel(4)
        >>> m.add(Cheese(1), 0)
        >>> m.get_number_of_cheeses()
        1
        """
        if self._stools[index]:
            if self._stools[index][-1].size < cheese.size:
                raise IllegalMoveError('Destination stool has a smaller' \
                                       ' cheese wheel!')
            else:
                self._stools[index].append(cheese)
        else:
            self._stools[index].append(cheese)

    def fill_first_stool(self, number_of_cheeses=3):
        """
        Adds however many given cheeses to the first stool in the model.

        @param TOAHModel self:
        @param cheeses int:
        @rtype: None

        >>> m = TOAHModel(4)
        >>> m.fill_first_stool(number_of_cheeses=7)
        >>> m.get_number_of_cheeses()
        7
        """
        for i in range(number_of_cheeses):
            self.add(Cheese(number_of_cheeses - i), 0)

class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool
        """
        if self.size == other.size:
            return True
        else:
            return False


class IllegalMoveError(Exception):
    """ Exception indicating move that violates TOAHModel
    """
    pass


class MoveSequence:
    """ Sequence of moves in TOAH game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def __eq__(self, other):
        """ Return whether MoveSequence self is equivalent to other.

        @param MoveSequence self:
        @param MoveSequence|Any other:
        @rtype: bool
        """
        return type(self) == type(other) and self._moves == other._moves
        
    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
