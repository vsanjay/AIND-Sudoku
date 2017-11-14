

# Assignments
rows = "ABCDEFGHI"    #Rows
cols = "123456789"    #Columns

def cross(A, B):      #will return the list formed by all the possible concatenations of a letter 's' in string A with a letter 't' in string B.
    "Cross product of elements in A and elements in B."

    return list(x + y for x in A for y in B)

boxes = cross(rows,cols)     #Individual Box Units Eg:- [A1,A2,A3,....B1,B2,.... etc]
row_units = list(cross(r,cols) for r in rows)  # All the row units Eg:- [[A1,A2,A3,....],[B1,B2,....]....]..
col_units = list(cross(rows,c) for c in cols)  #All the column units Eg:- [[A1,B1,C1...][A2,B2,C2....]]...
square_units = list(cross(rs,cs) for rs in ("ABC","DEF","GHI") for cs in ("123","456","789"))  #[['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],.....]
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['I1','H2','G3','F4','E5','D6','C7','B8','A9']] #Diagonal units
unit_list = row_units + col_units + square_units + diagonal_units # List of all units
units = dict((a,list(u for u in unit_list if a in u)) for a in boxes) # dictionary of units corresponding to particular box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Peers of corresponding box

def naked_twins(values):    #Implementing naked twins
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unit_list:      #Iterating along all units
        nkd_twins_num_individual = set()    #This set will hold a naked twin numbers as two seperate numbers.for Example '27' is one of the naked twin numbers,then our set will store '2','7' seperately.
        nkd_twins_num_full = set()          #This set will hold both naked twin numbers.

        for index_x,x in enumerate(unit):   #iterating through our respective unit.

            if len(values[x]) == 2:         #Checking if length of the value is 2 or not.
                for index_y,y in enumerate(unit):     # if length is 2,we are iterating our unit again to check if there is a duplicate of our number 'x' in our first for loop which will ultimately result to naked twins.
                    if (values[x] == values[y]) & (index_x != index_y): #This condition is to check if we found naked twins or not.Here,it is important to check indexes are different.
                        nkd_twins_num_individual.add(values[x][0])  #Adding numbers seperately to our set so that we can know what numbers do we need to delete later from the unit.
                        nkd_twins_num_individual.add(values[x][1])
                        nkd_twins_num_full.add(x)    #Here we add naked twin numbers to our set.
                        nkd_twins_num_full.add(y)

        if nkd_twins_num_individual:   #Checking if we found naked twin numbers.

            for x in unit:      #iterating through our unit so to remove the numbers from all boxes of our unit except the boxes containing naked twins.

                if (x in nkd_twins_num_full) |  (len(values[x]) == 1):  #checking if this box is naked twin box or not, as well as if length of the value is 1 or not so that we will not delete this number if length is one.
                    continue
                else:
                    for num in nkd_twins_num_individual:
                        values[x] = values[x].replace(num,"")   #Removing those numbers here and replacing with empty string.

    return values  #Finally returning values dictionary.



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81    #Checking if provided string length is 81 or not.
    dic = dict(zip(boxes,grid))

    for key in dic:
        if dic[key] == '.':
            dic[key] = "123456789"
        else:
            dic[key] = dic[key]
    return dic

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):       #This is to eliminate numbers from peers as well as emiminating values using naked twins technique..

    """Eliminate values from peers of each box with a single value and also elimiating numbers using naked twins technique.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.Then applying naked twin technique to
    eliminate more values.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_values = list(box for box in boxes if len(values[box]) == 1)

    for box in solved_values:
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box],'')  #Eliminating numbers which appear only once in our grid,from its peers.


    return naked_twins(values)   #Also observe here,We are also applying naked twin elimination here.Basically we are processing all elimination part here.Normal elimination as commented above as well as elimination using naked twin technique.

def only_choice(values):   #Function implementing only choice echnique.

    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unit_list:

        digits = "123456789"

        for digit in digits:
            arr = list(box for box in unit if digit in values[box])

            if len(arr) == 1:
                values[arr[0]] = digit

    return values

def reduce_puzzle(values):   #function

    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    stalled = False

    while stalled == False:

        solved_values_before = len(list(box for box in boxes if len(values[box]) == 1))

        eliminate(values)

        only_choice(values)

        solved_values_after = len(list(box for box in boxes if len(values[box]) == 1))

        stalled = solved_values_before == solved_values_after

        if len(list(box for box in boxes if len(values[box]) == 0)):
            return False

    return values

def search(values):

    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)

    if values == False:
        return False

    count = 0
    mini = 100
    minblock = ''

    for key in values:
        if len(values[key]) == 1:
            count += 1
        if (mini > len(values[key])) & (len(values[key]) > 1) :
            mini = len(values[key])   # Choose one of the unfilled squares with the fewest possibilities
            miniblock = key

    if count == 81:
        return values   ## Solved!

    for value in values[miniblock]:
        # Now use recurrence to solve each one of the resulting sudokus
        new_sudoku = values.copy()
        new_sudoku[miniblock] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))  #solving sudoku here

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))


    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
