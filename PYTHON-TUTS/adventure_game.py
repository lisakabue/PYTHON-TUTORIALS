def start_game():
    print("--- Welcome to the Explorer's Journey ---")
    print("You stand at a crossroads. Before you lie three paths.")
    
    # Prompting the player for a location
    choice = input("Where do you wish to go? (Forest / Cave / Beach): ").strip().lower()

    # Conditional statements to handle player choices
    if choice == "forest":
        print("\nYou step into the Forest. Sunlight filters through dense pine needles,")
        print("and the air is cool. You hear the faint sound of a distant wolf.")
        
    elif choice == "cave":
        print("\nYou venture into the Cave. It is damp and pitch black. Your footsteps")
        print("echo off the walls, and you see a faint glow deeper inside.")
        
    elif choice == "beach":
        print("\nYou walk onto the Beach. The salty breeze hits your face, and the")
        print("waves crash rhythmically against the shore. You spot a message in a bottle.")
        
    else:
        # Handling invalid inputs appropriately
        print(f"\n'{choice}' is not a valid path. You wander aimlessly in circles")
        print("until sunset. Please restart and choose a known destination.")

if __name__ == "__main__":
    start_game()
