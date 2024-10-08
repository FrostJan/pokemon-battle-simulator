import random
#FrostJan

# Pokemon lsit characters and their base powers
pokemon_list = {
    'Pikachu': 50,
    'Charmander': 55,
    'Bulbasaur': 60,
    'Squirtle': 58,
    'Jigglypuff': 45,
    'Eevee': 52,
    'Snorlax': 80,
    'Gengar': 70,
    'Machamp': 75,
    'Mewtwo': 90,
}

def calculate_power(base_power):
    
    # The power can be calculated as 
    # Final Power = base Power + Random Variation 
    variation = random.randint(-10, 10)
    return base_power + variation

def select_pokemon():

    # to select a Pokemon character
    while True:
        print("Choose your Pokémon:")
        for i, (pokemon, power) in enumerate(pokemon_list.items(), 1):
            print(f"{i}. {pokemon} (Base Power: {power})")
        try:
            choice = int(input("Enter the number corresponding to your Pokémon: "))
            if 1 <= choice <= len(pokemon_list):
                selected_pokemon = list(pokemon_list.keys())[choice - 1]
                return selected_pokemon, pokemon_list[selected_pokemon]
            else:
                print("Invalid input selection, please choose a valid number.")
        except ValueError:
            print("Invalid input, please enter a number.")

def battle(user_pokemon, user_power):

    # a random Pokemon for the computer
    opponent_pokemon, opponent_base_power = random.choice(list(pokemon_list.items()))
    opponent_power = calculate_power(opponent_base_power)

    print(f"\nYou chose {user_pokemon} with Power: {user_power}")
    print(f"Computer chose {opponent_pokemon} with Power: {opponent_power}")

    if user_power > opponent_power:
        print("You win this battle!")
        return user_pokemon, user_power + opponent_power, opponent_pokemon, opponent_power, 'User Wins'
    elif user_power < opponent_power:
        print("Computer wins this battle!")
        return user_pokemon, user_power - opponent_power, opponent_pokemon, opponent_power, 'Computer Wins'
    else:
        print("It's a tie!")
        return user_pokemon, user_power, opponent_pokemon, opponent_power, 'Tie'

def main():
    print("Welcome to the Pokémon Battle Simulator!")

    # to store each battle result
    battle_number = 0
    user_total_power = 0
    battle_results = []  
    win_count = 0
    loss_count = 0
    tie_count = 0

    # Pokemon selection
    user_pokemon, base_power = select_pokemon()
    user_power = calculate_power(base_power)

    while True:
        user_pokemon, user_power, opponent_pokemon, computer_power, status = battle(user_pokemon, user_power)

        battle_number += 1
        battle_results.append((battle_number, user_pokemon, user_power, opponent_pokemon, computer_power, status))

        if status == 'User Wins':
            win_count += 1
        elif status == 'Computer Wins':
            loss_count += 1
        else:
            tie_count += 1

        print(f"Battle {battle_number}: Your Pokémon Power: {user_power}, Status: {status.capitalize()}\n")

        next_step = input("Press 'c' to continue battling, 'n' for new Pokémon, or 'x' to exit: ").lower()
        if next_step == 'x':
            print("\nThank you for playing! Battle Summary:")
            print(f"{'Battle number':<15}{'User Pokémon (Power)':<25}{'Computer Pokémon (Power)':<30}{'Status'}")
            for result in battle_results:
                print(f"{result[0]:<15}{result[1]} ({result[2]}){'':<8}{result[3]} ({result[4]}){'':<8}{result[5]}")
            
            # battle Status
            if win_count > loss_count:
                battle_status = "User Wins"
            elif loss_count > win_count:
                battle_status = "Computer Wins"
            else:
                battle_status = "Tie"
                
            print(f"\nBattle Status: {battle_status}")
            break
        elif next_step == 'n':
            # to select a new Pokemon
            user_pokemon, base_power = select_pokemon()
            user_power = calculate_power(base_power)
        elif next_step == 'c':
            # Continue with the same Pokemon
            user_power = user_total_power  # Keep user current total power
        else:
            print("Invalid input, exiting the game.")
            break

if __name__ == "__main__":
    main()
