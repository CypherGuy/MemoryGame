import random
import time
import sys
import string
import sqlite3
import pandas as pd

letters = list(string.ascii_lowercase)
chosen_letters = []

#Initialise the sql bits

connection = sqlite3.connect('memory.db') #We have to always establish a connection to a database
cursor = connection.cursor() #Cursors allow you to execute SQL queries

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS memory (
        username,
        score INTEGER);''') #Here we create a table if one hasn't been made already.
connection.commit()#We have to commit, aka save out changes every time we change the table.

df = pd.read_sql_query("SELECT * FROM memory;", connection) #This is used to view our table in the Python terminal
print(df)

def timercalculation(level):
        time_formula = float(((0.0327380952381 * (level**2)) + (1.04761904762 * level) - 0.0803571428571))
        sleeptime = round(time_formula, 2)
        print(f'Time to wait = 10s')
        return sleeptime

class Competitor():#Let's initiate a class to keep stuff tidy

    def __init__(self, name, level = 1):
        self.name = name
        self.level = level

    def compare(self, color_list, player_input):
        if color_list == player_input:
            print(f"Congrats, you completed stage {player.level}. You're now going to do level {player.level + 1}") #Successful message
            player.level += 1
            time.sleep(2)
            return
        print(f"Nuh-uh, you have failed!\n\nYou wrote: {player_input}\nThe correct answer: {color_list}\n")#User gets pattern wrong
        time.sleep(4)
        print(f"Well you got to level {player.level}, but don't be sad if you are, you will do better next time!")#Final message before game ends
        player.save_to_db()
        sys.exit()#Ends the game

    def save_to_db(self):

        try: #Retrieve highscore
                playerlist = [str(f'{player.name}'), int(player.level) - 1] #We use this to try to locate the person and to check if they've beaten their highscore
                hs = cursor.execute(
                'SELECT * FROM memory WHERE username = ?;', (player.name,)
            )
                result = list(hs.fetchone())
                if result is None:
                    raise sqlite3.OperationalError

                if player.level > result[1]: #Highscore beaten
                    cursor.execute("""UPDATE memory SET score = ? WHERE username = ?;""", (playerlist[1], playerlist[0]))
                    connection.commit() #Remember to commit!
                    connection.close()
                    return print(f"Congrats on beating your highscore. You've improved from {result[1]} -> {player.level - 1}")
                else:
                    return print(f'You failed to beat your highscore of {result[1]}.')  

        except sqlite3.OperationalError or TypeError:#No highscore
            print(playerlist[0], playerlist[1])
            cursor.execute("""INSERT INTO memory VALUES (?,?)""", (playerlist[0], playerlist[1]))
            connection.commit()
            connection.close()
            return print(f"Since it's your first time, {player.name}, I've added your score of {player.level - 1} to the leaderboard.")   

def take_go(chosen_letters, counter, letters, level):
    print("Generating list of letters to memorise...")
    letters = [random.choice(letters) for _ in range(counter)]
    print("Generated!\n\n")

    c = random.randint(0, len(letters) - 1)
    chosen_letters.append(letters[c])

    color_list = ' '.join(chosen_letters) if len(chosen_letters) > 1 else ''.join(chosen_letters)
    
    print(f"You need to memorise this list of letters. Go!\n\n{color_list}")
    sleeptime = timercalculation(level)
    time.sleep(sleeptime)
    print("\n"*50)
    player_input = input("Done! Now enter what you saw, spaces and all: ")
    return color_list, player_input

#Main
if __name__ == "__main__":
    name = input("\n\nWhat's your username? ")
    player = Competitor(name) #Use of classes
    print(f"Wonderful {player.name}, nice to meet you! Let's get started.")

    while True:
        counter = player.level
        color_list, player_input = take_go(chosen_letters, counter, letters, player.level)
        player.compare(color_list, player_input)


