from art import logo
import random
import os

COIN = ['Heads', 'Tails']


def clear():
    os.system('cls')


def print_grid(game_grid):
    print(" 0  1  2")
    n = 0
    for line in game_grid:
        print(f'{line[0]} | {line[1]} | {line[2]}  {n}')
        n += 1
    print(' ')


def player_move(marker):
    column = ''
    row = ''
    while (row, column) in chosen_coordinates:
        while column != 0 and column != 1 and column != 2:
            column = input('Using the column numbers on top of the grid, pick your column: 0, 1 or 2:  ')
            if column != '0' and column != '1' and column != '2':
                print('Invalid Column Input')
            else:
                column = int(column)
        while row != 0 and row != 1 and row != 2:
            row = input('Using the row numbers to the right of the grid, pick your row: 0, 1 or 2: ')
            if row != '0' and row != '1' and row != '2':
                print('Invalid Row Input')
            else:
                row = int(row)
        if (row, column) in chosen_coordinates:
            print('Space already occupied, choose again')
            column = ''
            row = ''

    grid[row][column] = marker
    chosen_coordinates.append((row, column))


def check_win(game_grid, marker):
    winning_lines = [game_grid[0],
                     game_grid[1],
                     game_grid[2],
                     [game_grid[0][0], game_grid[1][0], game_grid[2][0]],
                     [game_grid[0][1], game_grid[1][1], game_grid[2][1]],
                     [game_grid[0][2], game_grid[1][2], game_grid[2][2]],
                     [game_grid[0][0], game_grid[1][1], game_grid[2][2]],
                     [game_grid[2][0], game_grid[1][1], game_grid[0][2]]
                     ]

    for winning_line in winning_lines:
        count = winning_line.count(marker)
        if count == 3:
            print(f'{marker} Wins!')
            return 'Game Over'

    empty_space = 0
    for row in grid:
        empty_space += row.count(' ')

    if empty_space == 0:
        print('There are no spaces left, the game is a tie!')
        return 'Game Over'


def two_player_game():
    playing = True
    coin_lands_on = random.choice(COIN)
    print(f'Heads X goes first, Tails O does.\nCoin landed on {coin_lands_on}')
    if coin_lands_on == 'Tails':
        print('O goes first!')
        print_grid(grid)
        while playing:
            player_move(marker='O')
            print_grid(grid)
            if check_win(game_grid=grid, marker='O') == 'Game Over':
                playing = check_if_play_again(two_player_game)
            else:
                player_move('X')
                print_grid(grid)
                if check_win(grid, 'X') == 'Game Over':
                    playing = check_if_play_again(two_player_game)
    else:
        print('X Goes first')
        print_grid(grid)
        while playing:
            player_move(marker='X')
            print_grid(grid)
            if check_win(game_grid=grid, marker='X') == 'Game Over':
                playing = check_if_play_again(two_player_game)
            else:
                player_move('O')
                print_grid(grid)
                if check_win(grid, 'O') == 'Game Over':
                    playing = check_if_play_again(two_player_game)


def ai_check_for_nearly_finished_line(game_grid, marker):
    global blank_space
    winning_lines = [[(0, 0), (0, 1), (0, 2)],
                     [(1, 0), (1, 1), (1, 2)],
                     [(2, 0), (2, 1), (2, 2)],
                     [(0, 0), (1, 0), (2, 0)],
                     [(0, 1), (1, 1), (2, 1)],
                     [(0, 2), (1, 2), (2, 2)],
                     [(0, 0), (1, 1), (2, 2)],
                     [(2, 0), (1, 1), (0, 2)]
                     ]
    for line in winning_lines:
        x_count = 0
        blank_count = 0
        for coordinate in line:
            if game_grid[coordinate[0]][coordinate[1]] == 'X':
                x_count += 1
            elif game_grid[coordinate[0]][coordinate[1]] == ' ':
                blank_space = coordinate
                blank_count += 1
        if x_count == 2 and blank_count == 1:
            game_grid[blank_space[0]][blank_space[1]] = marker
            chosen_coordinates.append((blank_space[0], blank_space[1]))
            return True
    for line in winning_lines:
        o_count = 0
        blank_count = 0
        for coordinate in line:
            if game_grid[coordinate[0]][coordinate[1]] == 'O':
                o_count += 1
            elif game_grid[coordinate[0]][coordinate[1]] == ' ':
                blank_space = coordinate
                blank_count += 1
        if o_count == 2 and blank_count == 1:
            game_grid[blank_space[0]][blank_space[1]] = marker
            chosen_coordinates.append((blank_space[0], blank_space[1]))
            return True


def ai_move(game_grid, marker):
    global blank_space
    print('Computer Move:')
    turn = len(chosen_coordinates)
    last_player_move = chosen_coordinates[-1]
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    if turn == 1:
        game_grid[0][0] = marker
        chosen_coordinates.append((0, 0))
    elif turn == 2 and last_player_move in corners:
        game_grid[1][1] = marker
        chosen_coordinates.append((1, 1))
    elif turn == 2:
        game_grid[0][0] = marker
        chosen_coordinates.append((0, 0))
    elif turn == 3 and last_player_move == (1, 1):
        game_grid[2][2] = marker
        chosen_coordinates.append((2, 2))
    elif turn == 3 and last_player_move != (1, 1):
        if last_player_move == (0, 1) or last_player_move == (0, 2)\
                or last_player_move == (1, 2) or last_player_move == (2, 2):
            game_grid[2][0] = marker
            chosen_coordinates.append((2, 0))
        elif last_player_move == (1, 0) or last_player_move == (2, 0) or last_player_move == (2, 1):
            game_grid[0][2] = marker
            chosen_coordinates.append((0, 2))
    elif turn >= 4:
        if ai_check_for_nearly_finished_line(game_grid, marker):
            pass
        elif (1, 1) not in chosen_coordinates:
            game_grid[1][1] = marker
            chosen_coordinates.append((1, 1))
        else:
            for coordinate in corners:
                if coordinate not in chosen_coordinates:
                    game_grid[coordinate[0]][coordinate[1]] = marker
                    chosen_coordinates.append(coordinate)
                    return
            for coordinate in edges:
                if coordinate not in chosen_coordinates:
                    game_grid[coordinate[0]][coordinate[1]] = marker
                    chosen_coordinates.append(coordinate)
                    return
    print_grid(grid)


def single_player_game():
    playing_ai = True
    coin_result = random.choice(COIN)
    print(f'If Coin lands on Heads, AI goes first. If Tails You go First.\nCoin lands on {coin_result}')
    if coin_result == 'Tails':
        print("You go first, you're playing as O.")
        print_grid(grid)
        while playing_ai:
            player_move('O')
            if check_win(grid, 'O') == 'Game Over':
                playing_ai = check_if_play_again(single_player_game)
            else:
                print_grid(grid)
                ai_move(grid, 'X')
                if check_win(grid, 'X') == 'Game Over':
                    playing_ai = check_if_play_again(single_player_game)
    if coin_result == 'Heads':
        print("AI goes first, you're playing as O.")
        while playing_ai:
            ai_move(grid, 'X')
            if check_win(grid, 'X') == 'Game Over':
                playing_ai = check_if_play_again(single_player_game)
            else:
                player_move('O')
                print_grid(grid)
                if check_win(grid, 'O') == 'Game Over':
                    playing_ai = check_if_play_again(single_player_game)


def check_if_play_again(game):
    global grid, chosen_coordinates
    play_again = input('Would you like to play again? [y/n]: ').lower()
    if play_again == 'y':
        grid = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        chosen_coordinates = [('', '')]
        game()
    elif play_again == 'n':
        return False
    else:
        print('Invalid input, returning to main menu.')
        return False


game_on = True
while game_on:
    grid = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    chosen_coordinates = [('', '')]
    print(logo)
    game_choice = input('Choose the number of the game you would like to play:'
                        '\n1. Single Player against an AI'
                        '\n2. Two Player against each other'
                        '\n3. Exit Game\n')

    if game_choice == '1':
        blank_space = ''
        single_player_game()
    elif game_choice == '2':
        two_player_game()
    elif game_choice == '3':
        game_on = False
    else:
        print('That is not a valid option.')
