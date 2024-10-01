from Player.player import Player
import time

def welcome():
    print("\n---------------------------------------------\n")
    print("You wake up in a dark, eerie forest...")
    time.sleep(2)
    print("The wind howls through the trees, and the air is thick with mist.")
    time.sleep(2)
    print("You hear footsteps approaching from behind, but before you can react, a chilling voice whispers...")
    time.sleep(3)
    print("\nYou: \"Who's that...\"\n")
    time.sleep(2)
    print("Witch: \"Welcome, foolish traveler...\"")
    time.sleep(2)
    print("Witch: \"You have wandered into my domain, and there is no escape.\"")
    time.sleep(3)
    print("Witch: \"The forest is alive with danger, and I, the Witch of Shadows, have sealed your fate.\"")
    time.sleep(3)
    print("Witch: \"However... if you can find the exit hidden deep within this forest, you may survive.\"")
    time.sleep(3)
    print("\n\"You: I'll find my way, and you'll be punished for your deeds...\"\n")
    time.sleep(2)
    print("Witch: \"But beware... for every step you take, I will be watching.\"")
    time.sleep(2)
    print("\n\"You: Don't underestimate me!\"\n")
    time.sleep(2)
    print("\"Witch: Good luck then...\"\n \n---The voice fades into the night as you stand alone---")
    time.sleep(3)
    print("\n> Your journey begins now... find the exit, or be trapped forever.\n")
    time.sleep(2)
    print("\n---------------------------------------------\n")

def initalize():
    player = Player()
    print("Enter your choice:\n1. Start a new game.\n2. Load previous game.")
    choice = int(input())
    while True:
        if choice ==1:
            player.get_name()
            return player
        elif choice ==2:
            name = input("Enter player name to load game.")
            player = player.load_game()
            return player
        else: print("Invalid input, try again")

def main():
    welcome()
    player = initalize()

    print("-------------------Welcome to the 'Haunted Forest Adventure'-------------------------")
    print("You find yourself standing at the campsite. And In front of you is a 'Dark forest' ")
    print("Find a way to exit the forest")
    print("You can go in the following directions:")
    print("-north")
    print("-south")
    print("-east")
    print("-west")
    print("And you can use the following commands: ")
    print("-Move (To move in the given directions)")
    print("-Examine (To examine some area. You can get some clues by examining)")
    print("-Search (For searching in that area)")
    print("-Look (To look at your surroundings or to get a description about the area.)")
    print("-Pick (To pick an item and store it in the inventory)")
    print("-Drop (To drop an item from the inventory)")
    print("-Use (To use an item from the inventory.)")
    print("-See Inventory (To see items in your inventory)")

    while True:
        print("What would you like to do ? ")
        print("Just enter the number of the command you like to perform:")
        print("1.Move\n2.Examine\n3.Search\n4.Look\n5.Pick\n6.Drop\n7.Use\n8.See inventory\n9.Save Game\n10.Quit Game")
        user_input = int(input("Enter the number of command."))
        
        if user_input == 1:
            direction = input("In which direction do you want to move?")
            player.move(direction)
        elif user_input == 2:
            print("Keep in mind that only the objects of the current locations will be examined")
            print("You can also examine your current area, which might be helpful in finding some clues.")
            print("So you want to examine the objects or the current area?")
            print("1.current area\n2.object")
            user_in = int(input("Enter your choice: "))
            if user_in == 1:
                player.examine(player.current_location)
            elif user_in == 2:
                print("Which of the following objects do you want to examine:")
                print("1.half torn paper")
                print("2.tree")
                print("3.shining thing")
                print("4.strange nest")
                print("5.path")
                print("6.fireplace")
                print("7.wooden object")
                print("8.cave wall")
                print("9.wall hanging")
                print("10.ancient box")
                user_num = int(input("Enter your choice: "))
                if user_num == 1:
                    player.examine("half torn paper")
                elif user_num == 2:
                    player.examine("tree")
                elif user_num == 3:
                    player.examine("shining thing")
                elif user_num == 4:
                    player.examine("strange nest")
                elif user_num == 5:
                    player.examine("path")
                elif user_num == 6:
                    player.examine("fireplace")
                elif user_num == 7:
                    player.examine("wooden object")
                elif user_num == 8:
                    player.examine("cave wall")
                elif user_num == 9:
                    player.examine("wall hanging")
                elif user_num == 10:
                    player.examine("ancient box")

           
        elif user_input == 3:
            items = player.search(player.current_location)
            if items:
                print("Items found: " + items)
                user_choice = input("Do you want to pick these items? Type 'yes' or 'no'")
                if user_choice == "yes":
                    for item in items:
                        player.pick(item)
                else:
                    print("You didn't pick the items! You might need them")
            else:
                print("No items found in this area.")                 
        elif user_input == 4:
            player.look()

        elif user_input == 5:
            user_item = input("Which item do you want to pick?")
            player.pick(user_item)    
        elif user_input == 6:
            print(", ".join(player.inventory))
            item_to_drop = input("Which item do you want to drop? ")
            player.drop_item(item_to_drop)

        elif user_input == 7:
            print(", ".join(player.inventory))
            item_to_use = input("Which item do you want to use ?")
            player.use(item_to_use)

        elif user_input == 8:
            print("The following items are in your inventory: ")
            print(", ".join(player.inventory))
        elif user_input == 9:
            player.save_game()  
            return  
        elif user_input == 10:
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    # welcome()
    main()