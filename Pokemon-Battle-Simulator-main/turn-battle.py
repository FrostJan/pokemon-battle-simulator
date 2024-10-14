import random
import pandas as pd

# Load Pokémon dataset
pokemon_data = pd.read_csv('Pokemon.csv')

# Function to select a Pokémon
def select_pokemon(player):
    while True:
        print(f"{player}, select your Pokémon by typing its name:")
        selected_pokemon_name = input().strip()
        if selected_pokemon_name in pokemon_data['Name'].values:
            return pokemon_data[pokemon_data['Name'] == selected_pokemon_name].iloc[0].to_dict()
        else:
            print("Invalid Pokémon name, please try again.")

# Function to simulate a turn-based Pokémon battle
def battle(pokemon1, pokemon2):
    print(f"Battle Start! {pokemon1['Name']} vs {pokemon2['Name']}")
    
    # Battle loop
    while pokemon1['HP'] > 0 and pokemon2['HP'] > 0:
        # Determine which Pokémon goes first based on Speed
        if pokemon1['Speed'] > pokemon2['Speed']:
            attacker, defender = pokemon1, pokemon2
        else:
            attacker, defender = pokemon2, pokemon1
        
        # Attack sequence
        attack_value = random.choice([attacker['Attack'], attacker['Sp. Atk']])
        defense_value = random.choice([defender['Defense'], defender['Sp. Def']])
        
        # Damage calculation: (Attack - Defense) with a minimum of 1 damage
        damage = max(1, attack_value - defense_value)
        defender['HP'] -= damage
        
        print(f"{attacker['Name']} attacks {defender['Name']} causing {damage} damage!")
        print(f"{defender['Name']} has {defender['HP']} HP left.")
        
        # Check if defender is defeated
        if defender['HP'] <= 0:
            print(f"{defender['Name']} is knocked out!")
            print(f"{attacker['Name']} wins the battle!")
            break
        
        # Switch roles for the next turn
        pokemon1, pokemon2 = pokemon2, pokemon1

# Main game logic
def main():
    print("Welcome to the Pokémon Battle Simulator!")
    
    # Player 1 selects Pokémon
    pokemon1 = select_pokemon("Player 1")
    
    # Player 2 selects Pokémon
    pokemon2 = select_pokemon("Player 2")
    
    # Start the battle
    battle(pokemon1, pokemon2)

if __name__ == "__main__":
    main()
