from GameStructure.map import forest_map
from GameStructure.riddles import riddles
from GameStructure.examined_areas import examined_areas, location_access
from random import randint
import json


class Player:
    def __init__(self):
        self.name = None
        self.current_location = 'Campsite'  
        self.inventory = []  
        self.score = 0
        self.max_inventory_size = 4 
        self.game_history = []
        self.map = forest_map
        self.current_riddle = None
        self.riddles = riddles
        self.examined_areas = examined_areas
        self.location_access = location_access

    def get_name(self):
        name = input('Enter your name:')
        self.name = name

    def look(self):
        print(f"--{self.map[self.current_location]['description']}--")
        exits = self.map[self.current_location]['exits']
        print(f'Exits: ')
        for direction, place in exits.items():
            print(f"({direction}) -> {place}")
    
    def move(self,direction):

        if direction in forest_map[self.current_location]['exits']:
            new_location = forest_map[self.current_location]['exits'][direction]
        
        # Check for restricted areas
            if new_location == 'Old Cabin':
                if "key" in self.inventory:
                    self.location_access['Old Cabin'] = True
                    self.use("key")
                else:
                    print("The cabin door is locked. You need a key to enter.")
        
            elif new_location == 'Small Hut':
                if examined_areas['Dark Woods']['path']:
                    print("You found a small hut hidden in the woods.")
                    self.location_access['Small Hut'] = True
                    self.current_location = new_location
                    print(f"You moved to the {new_location}.")
                else:
                    print("You haven't discovered the path to the Small Hut yet.")
        
            elif new_location == 'Hidden Cave':
                if examined_areas['Hidden Cave']['cave_tree']:
                    self.location_access['Hidden Cave'] = True
                    self.use("axe")
                else:
                    print("There seems to be a tree blocking the entrance. You need to examine it first.")
                    
            elif new_location == "Witch's Hut":
                print(forest_map["Witch's Hut"]['description'])
                print("The witch says \"you have to answer 3 riddles and in return I will give you something valuable\"")
                print("You have 6 attempts and then you will be killed by the witch and game over! ")
                print("Answer the riddle. ")
                counter = 0
                for i in range(0,6):
                    self.generate_riddle()
                    print("What is your answer or you want a clue ?")
                    user_choice = int(input("1.answer\n2.clue"))
                    if user_choice == 1:
                        user_answer = input("Write your answer")
                        if self.solve_riddle(user_answer):
                            print("Correct! You've solved the riddle.")
                            counter+=1
                            if counter == 3:
                                print("You have been given an axe by the witch and she also gives an hint: 'Check for the trees, they might be hiding some entrance, maybe some hidden cave.'")
                                self.inventory.append("axe")
                                break
                        else:
                            print("Incorrect answer. Try again.")

                    elif user_choice == 2:
                        self.riddle_clue(self.current_riddle['question']) 
                        user_answer = input("Write your answer")
                        if self.solve_riddle(user_answer):
                            print("Correct! You've solved the riddle.")
                            counter+=1
                            if counter == 3:
                                print("You have been given an axe by the witch and she also gives an hint: 'Check for the trees, they might be hiding some entrance, maybe some hidden cave.'")
                                self.inventory.append("axe")
                                self.move('Hidden Cave')
                                break
                        else:
                            print("Incorrect answer. Try again.")                           
           
            else:
                self.current_location = new_location
                print(f"You moved to the {new_location}.")
                print(forest_map[self.current_location]['description'])
        else:
            print(f"You can't move {direction} from here.")

    def search(self,location):

        found_items = []

        if location == 'Campsite' and self.examined_areas['Campsite']['half torn paper']:
            found_items = forest_map['Campsite']['items']
    
        elif location == 'Dark Woods':
            if self.examined_areas['Dark Woods']['tree']:
                found_items.append('key')
            if self.examined_areas['Dark Woods']['shining thing']:
                found_items.append('jewel')
            if self.examined_areas['Dark Woods']['strange nest']:
                found_items.append('key')
    
        elif location == 'Small Hut':
            # All items are discoverable without examination
            found_items = forest_map['Small Hut']['items']
    
        elif location == 'Old Cabin' and self.examined_areas['Old Cabin']['fireplace']:
            found_items = ['rare piece of a key']
    
        elif location == 'Riverbank' and self.examined_areas['Riverbank']['wooden object']:
            found_items = ['raft']
    
        elif location == 'Hidden Cave':
            if self.examined_areas['Hidden Cave']['cave wall']:
                found_items.append('ancient box')
            if self.examined_areas['Hidden Cave']['wall hanging']:
                found_items.append('rare piece of a key')

        if found_items:
            return found_items

    def pick(self, item):
        if item in self.map[self.current_location]['items']:
            if len(self.inventory) < self.max_inventory_size:
                self.inventory.append(item)
                self.map[self.current_location]['items'].remove(item)
                print(f"{item} added to your inventory.")
            else:
                print("Inventory full! Drop an item to make space.")
        else:
            print(f"{item} not found here.")

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.map[self.current_location]['items'].append(item)
            
            print(f"You have dropped {item}. It is now in {self.current_location}.")
        else:
            print(f"You don't have {item} in your inventory.")

    def use(self,item):

        if item in self.map[self.current_location]['items']:
            if item == 'Match':
                if self.current_location == 'Campsite' and 'lantern' in self.inventory:
                    print("You used the match to light up the lantern. You can now drop the match if you want.")
                else:
                    print("You can not use match")    
            elif item == 'key' and 'key' in self.inventory:
                if self.current_location == 'Old Cabin':
                    print("You've used the key to open the Old Cabin. You can now discard the key.")
                    self.current_location = self.map['Old Cabin']
                    print("You are  in the Old Cabin now")
                else:
                    print("You can not use the key here. You can use it to open the old cabin")    

            elif item == 'jewel':
                if self.current_location == "Witch's Hut" and 'jewel' in self.inventory: 
                    print("You've given the jewel to the witch ")
                    self.inventory.remove(item)
                else:
                    print("You can not use the jewel here.")
            elif item == 'Shovel':
                if self.current_location == "Riverbank" and 'Shovel' in self.inventory:
                    print("You've used the shovel to dig the ground. You found a raft on which you can go to the other side of the river.")
                    self.inventory.append("raft")
                else:
                    print("You can not use the shovel here")    

            elif item == 'rare piece of a key':
                if self.current_location == "Hidden Cave" and 'rare piece of a key':
                    if self.inventory.count("rare piece of a key") == 2:
                        print("You've combined the rare pieces to form a key")
                        self.inventory.append("Rare key")
                    else:
                        print("Not enough pieces to join. Search for the other piece to form a key.")
                else:
                    print("You can not join the pieces")                    

            elif item == 'raft':
                if self.current_location == "Riverbank" and 'raft' in self.inventory: 
                    print("You've used the raft to cross the river. You are now on the other side of river. You can discard the raft now.")
                    print("There is a strange creepy hut nearby. Looks like its a witch's hut.")
                    self.current_location = self.map['Witch’s Hut']
                    print(self.map['Witch’s Hut']['description'])
                else:
                    print("You can not use the raft")    

            elif item == 'axe':
                if 'axe' in self.inventory:
                    print("You've used the axe to cut down the tree. The Entrance to the hidden cave is now open. You can discard the axe now")
                    self.current_location = self.map['Hidden Cave']
                    print(self.map['Hidden Cave']['description'])
                else:
                    print("You can not use the axe here")    
                
            elif item == "Rare key":
                if self.current_location == "Hidden Cave" and 'Rare key' in self.inventory:
                    print("You've used the rare key to open the secret door.")
                    self.current_location = self.map['Tunnel']
                    print(self.map['Tunnel']['description'])
                else:
                    print("You can not use the rare key here")    
  
    def show_inventory(self):
        if self.inventory:
            print("Your inventory contains:", ', '.join(self.inventory))
        else:
            print("Your inventory is empty.")

    def update_score(self, points):
        self.score += points
        print(f"Your score is now: {self.score}")
    # 
    def generate_riddle(self):
        range = 5
        random_number = randint(0, range)
        self.current_riddle = self.riddels[random_number]["question"]
        self.riddels.pop(random_number) 
        print(self.current_riddle)
        range -= 1

    def solve_riddle(self, answer):
        if self.current_riddle and answer.lower() == self.current_riddle["answer"]:
            self.current_riddle = None
            return True
        else:
            return False


    def riddle_clue(self, question):
        user_input = input("You have to give jewel to witch in return for clues. (Yes/No)?")
        if user_input.lower() == "yes":
            if "jewel" in self.inventory:
                self.inventory.remove("jewel")
                if question == riddles[0]["question"]:
                    print(riddles[0]["clue"])
                elif question == riddles[1]["question"]:
                    print(riddles[1]["clue"])
                elif question == riddles[2]["question"]:
                    print(riddles[2]["clue"])
                elif question == riddles[3]["question"]:
                    print(riddles[3]["clue"])
                elif question == riddles[4]["question"]:
                    print(riddles[4]["clue"])
                elif question == riddles[5]["question"]:
                    print(riddles[5]["clue"])

            else:
                print("You don't have a jewel in the inventory")
                print("If you still want to get clues, your score will be deducted (-10)")
                user_response = input("Do you still want to get clues?")
                if user_response.lower() == "yes":
                    self.deduct_score()
                    if question == riddles[0]["question"]:
                        print(riddles[0]["clue"])
                    elif question == riddles[1]["question"]:
                        print(riddles[1]["clue"])
                    elif question == riddles[2]["question"]:
                        print(riddles[2]["clue"])
                    elif question == riddles[3]["question"]:
                        print(riddles[3]["clue"])
                    elif question == riddles[4]["question"]:
                        print(riddles[4]["clue"])
                    elif question == riddles[5]["question"]:
                        print(riddles[5]["clue"])

    def examine(self, object):
        object = object.lower()
        if self.current_location == 'Campsite' and object == 'half torn paper':
            print(f"There is something written on the paper: {forest_map['Campsite']['clue']}")
            examined_areas['Campsite']['half torn paper'] = True

        elif self.current_location == 'Dark Woods':
            if object == 'tree':
                print(forest_map['Dark Woods']['clue1'])
                examined_areas['Dark Woods']['tree'] = True
            elif object == 'shining thing':
                print("It is a rare jewel. Maybe you can use it in return for something.")
                examined_areas['Dark Woods']['shining thing'] = True
            elif object == 'strange nest':
                print("The nest looks like to have something in it... It's an old key. Maybe you can use it to open the cabin.")
                examined_areas['Dark Woods']['strange nest'] = True
            elif object == 'path':
                print("The path is going towards a small hut. Maybe you can find something in the hut.")
                examined_areas['Dark Woods']['path'] = True

        elif self.current_location == 'Old Cabin' and object == 'fireplace':
            print("A rare piece of something is placed there. Looks like it is combined with another piece to form a key.")
            examined_areas['Old Cabin']['fireplace'] = True

        elif self.current_location == 'Riverbank' and object == 'wooden object':
            print("It looks like an old raft. But it's half under the ground.")
            examined_areas['Riverbank']['wooden object'] = True

        elif self.current_location == 'Hidden Cave':
            if object == 'cave wall':
                print("There are some arrows on the wall and against each arrow there is a number.")
                print("Just like this: <- 3, -> 4, <- 2.")
                examined_areas['Tunnel']['cave wall'] = True
            elif object == 'wall hanging':
                print("Looks like the wall hanging can be removed.")
                examined_areas['Tunnel']['wall hanging'] = True
            elif object == 'ancient box':
                print("There is a combination lock on this box. You might find something valuable in it ")
                user_response = input("Do you want to apply the combination? Type 'yes' or 'no'")
                if user_response == "yes":
                    while True:
                        print("Add the number for each movement:")
                        num1 = int(input("left"))
                        num2 = int(input("right"))
                        num3 = int(input("left"))
                        if num1 == 3 and num2 == 4 and num3 == 2:
                            print("Correct! the box is opening")
                            print("It has a rare piece of key")
                            self.inventory.append("rare piece of a key")
                            break
                        else:
                            print("wrong combination! try again.")

        else:
            print("There's nothing to examine here.")

    def deduct_score():
        global score
        score-=10   

    def to_dict(self):
        return {
            'name': self.name,
            'current_location': self.current_location,
            'inventory': self.inventory,
            'score': self.score,
            'max_inventory_size': self.max_inventory_size,
            'game_history': self.game_history,
            'map': self.map,
            'current_riddle': self.current_riddle,
            'riddles': self.riddles,
            'examined_areas': self.examined_areas,
            'location_access': self.location_access
        }

    def save_game(self, file_name='game_data.json'):
        try:
            with open(file_name, 'r') as file:
                players_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            players_data = {}

        if self.name in players_data:
            print(f"Player with name '{self.name}' already exists. Choose a different name.")
            self.name = input()
            print('Name changed,try saving again')
            return

        players_data[self.name] = self.to_dict()

        with open(file_name, 'w') as file:
            json.dump(players_data, file, indent=4)

        print(f"Game saved for player '{self.name}'.")
    @classmethod
    def load_game(self, file_name='game_data.json'):
        try:
            with open(file_name, 'r') as file:
                players_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No saved game data found in '{file_name}'.")
            return

        if self.name not in players_data:
            print(f"No saved game found for player '{self.name}'.")
            return

        player_data = players_data[self.name]
        self.current_location = player_data['current_location']
        self.inventory = player_data['inventory']
        self.score = player_data['score']
        self.max_inventory_size = player_data['max_inventory_size']
        self.game_history = player_data['game_history']
        self.map = player_data['map']
        self.current_riddle = player_data['current_riddle']
        self.riddles = player_data['riddles']
        self.examined_areas = player_data['examined_areas']
        self.location_access = player_data['location_access']

        print(f"Game loaded for player '{self.name}'.")

    