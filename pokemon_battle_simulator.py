import random
from tabulate import tabulate

class Pokemon:
    def __init__(self, name, types, strong_against, weak_against):
        self.name = name
        self.types = types
        self.strong_against = strong_against
        self.weak_against = weak_against
        self.hp = random.uniform(40, 50)  # HP between 40 and 50
        self.power = random.randint(9, 10)  # Attack power between 7 and 10
        self.is_defending = False
        self.defense_turns = 0  # Track number of turns defense is active
        self.poisoned = False
        self.poison_damage = 0
        self.poison_turns = 0
        self.heal_used = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        # Check for critical hit
        if random.random() < 0.1:  # 10% chance for a critical hit
            damage *= 2
            print("Critical hit!")

        if self.is_defending and self.defense_turns < 2:
            damage *= 0.75  # Reduce damage by 25% if defending
            self.defense_turns += 1
            if self.defense_turns == 2:
                self.is_defending = False  # Reset defense after two attacks

        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self):
        if not self.heal_used:
            self.hp += 20  # Heal by 20 HP
            if self.hp > 100:  # Assuming max HP is 100
                self.hp = 100
            self.heal_used = True

    def apply_poison(self):
        if self.poison_turns < 2:
            self.poisoned = True
            self.poison_damage = random.uniform(3.50, 5.00)  # Poison damage between 3.50 and 5.00
            self.poison_turns += 1

    def take_poison_damage(self):
        if self.poisoned:
            self.hp -= self.poison_damage
            if self.hp < 0:
                self.hp = 0
            self.poison_turns -= 1
            if self.poison_turns == 0:
                self.poisoned = False  # Reset poison status after 2 turns

    def fatigue(self):
        if self.hp <= 30 and self.hp > 10:  # Check if the Pokémon's condition is "Fatigue" and HP is more than 10
            fatigue_amount = 5  # Fixed fatigue amount
            self.take_damage(fatigue_amount)
            return fatigue_amount  # Return the amount of health lost due to fatigue
        return 0  # No fatigue if condition is not "Fatigue" or HP is less than or equal to 10

    def calculate_damage(self, opponent):
        damage = self.power
        multiplier = 1.0  # Default multiplier
        if any(t in opponent.weak_against for t in self.types):
            damage *= 1.5  # Strong against
            multiplier = 1.5
        elif any(t in opponent.strong_against for t in self.types):
            damage *= 0.5  # Weak against
            multiplier = 0.5
        return damage, multiplier  # Return both damage and multiplier
    
def print_centered_header(header):
    max_length = 100
    print()  # Extra space above
    centered_header = header.center(max_length, '-')
    print(centered_header)
    print()  # Extra space below

def display_battle_status(pokemon, player_name, poison_pots, healing_pots):
    print_centered_header(f"{player_name} Turn")
    condition = "Good" if pokemon.hp > 30 else "Fatigue" if pokemon.hp > 0 else "Fainted"
    queue_status = "A" if pokemon.hp < 30 else "NA"
    print(tabulate([[pokemon.name, "/".join(pokemon.types), f"{pokemon.hp:.2f}", condition]],
                   headers=["Pokémon Name", "Type", "Health", "Condition"], tablefmt="grid", stralign="center"))
    
    # Display Actions 
    actions_data = [["Attack(Z)", "Defense(X)", f"Poison Pot(C): {poison_pots}", f"Healing Pot(V): {healing_pots}", f"Queue(B): {queue_status}"]]
    print("\nActions")
    print(tabulate(actions_data, tablefmt="grid", stralign="center"))

def queue_mode(player_name, active_pokemon, pokemons, opponent_pokemon):
    if active_pokemon.hp > 30:
        print("Cannot switch Pokémon unless health is below 60%.")
        return active_pokemon

    display_queue(player_name, pokemons)
    while True:
        try:
            choice = int(input(f"{player_name}, choose a new Pokémon to switch to (1-{len(pokemons)}): ")) - 1
            if 0 <= choice < len(pokemons) and pokemons[choice].is_alive() and pokemons[choice] != active_pokemon:
                pokemon_before = active_pokemon.hp
                opponent_before = opponent_pokemon.hp

                active_pokemon.hp = max(0, active_pokemon.hp - 15)
                opponent_pokemon.hp = min(50, opponent_pokemon.hp + 10)

                switch_hp_change = {
                    'pokemon_before': pokemon_before,
                    'pokemon_after': active_pokemon.hp,
                    'opponent_before': opponent_before,
                    'opponent_after': opponent_pokemon.hp
                }

                display_action_result(player_name, "b", active_pokemon, opponent_pokemon, switch_hp_change=switch_hp_change)
                return pokemons[choice]
            else:
                print("Invalid choice or Pokémon is fainted. Please choose again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_queue(player_name, pokemons):
    print_centered_header(f"Queue(Mode) for {player_name} Pokémon List")
    table_data = [
        [i + 1, pokemon.name, "/".join(pokemon.types), f"{max(0, pokemon.hp):.2f}", pokemon.power, 
         "Good" if pokemon.hp > 30 else "Fatigue" if pokemon.hp > 0 else "Fainted"]
        for i, pokemon in enumerate(pokemons)
    ]
    print(tabulate(table_data, headers=["No", "Name", "Type", "Health", "Dmg", "Condition"], tablefmt="grid", stralign="center"))

def display_action_result(player_name, action, pokemon, opponent, damage=None, switch_hp_change=None, multiplier=None):
    print_centered_header(f"{player_name} Action")
    if action == "z" and damage is not None:
        poison_effect = f" and inflicting poison damage!" if opponent.poisoned else ""
        fainted_status = " Fainted!!" if opponent.hp <= 0 else ""
        action_detail = f"{pokemon.name} attacks{(' (SA)' if multiplier == 1.5 else ' (WA)' if multiplier == 0.5 else '')} {opponent.name} causing {damage:.2f} damage! {opponent.hp + damage:.2f} > {opponent.hp:.2f}{fainted_status}"
    elif action == "v":
        action_detail = f"{pokemon.name} heals, restoring health! {pokemon.hp - 20:.2f} > {pokemon.hp:.2f}"
    else:
        action_details = {
            "x": f"{pokemon.name} is defending, reducing incoming damage!",
            "c": f"{pokemon.name} poisons {opponent.name}, inflicting poison damage!",
            "b": f"{pokemon.name} switches out, changing the battle dynamics!"
        }
        action_detail = action_details.get(action, "Invalid action!")

    # Calculate fatigue and add to action result
    fatigue_amount = pokemon.fatigue()
    if fatigue_amount > 0:
        fatigue_detail = f"{pokemon.name} loses {fatigue_amount:.2f} health due to fatigue {pokemon.hp + fatigue_amount:.2f} > {pokemon.hp:.2f}"
        result_data = [[action_detail], [fatigue_detail]]
    else:
        result_data = [[action_detail]]

    # Add switch out message if action is 'b'
    if action == "b" and switch_hp_change:
        switch_detail = f"{pokemon.name} is switched out, losing 15 HP {switch_hp_change['pokemon_before']:.2f} > {switch_hp_change['pokemon_after']:.2f}. {opponent.name} gains 10 HP {switch_hp_change['opponent_before']:.2f} > {switch_hp_change['opponent_after']:.2f}."
        result_data.append([switch_detail])
                
    print(tabulate(result_data, tablefmt="grid", stralign="center"))

def display_battle_results(battle_results):
    print_centered_header("Fight Results")
    scores = {"P1": 0, "P2": 0}
    result_data = []

    for result in battle_results:
        player, pokemon1, pokemon2, winner = result
        if winner == "P1":
            scores["P1"] += 1
            result_data.append([player, f"{pokemon1} win against {pokemon2}", 1, 0])
        else:
            scores["P2"] += 1
            result_data.append([player, f"{pokemon2} win against {pokemon1}", 0, 1])

    # Final score
    result_data.append(["Final Score", "", scores["P1"], scores["P2"]])

    # Print results
    print("\n" + tabulate(result_data, headers=["Player #", "Result", "Score", "Score"], tablefmt="grid"))

def battle(pokemon1, pokemon2, player1_name, player2_name, player1_pokemons, player2_pokemons):
    player1_poison_pots = 3
    player1_healing_pots = 3
    player2_poison_pots = 3
    player2_healing_pots = 3

    # Track the results of each fight
    fight_results = []

    while True:
        # Player 1's turn
        while True:
            display_battle_status(pokemon1, player1_name, player1_poison_pots, player1_healing_pots)
            action1 = input("Choose Action: ").strip().lower()

            if action1 == "z":
                damage, multiplier = pokemon1.calculate_damage(pokemon2)
                pokemon2.take_damage(damage)
                display_action_result(player1_name, action1, pokemon1, pokemon2, damage, multiplier=multiplier)
                break
            elif action1 == "x":
                pokemon1.is_defending = True
                pokemon1.defense_turns = 0  # Reset defense turns
                display_action_result(player1_name, action1, pokemon1, pokemon2)
                break
            elif action1 == "c":
                if player1_poison_pots > 0:
                    if not pokemon1.poisoned and pokemon1.poison_turns < 3:
                        pokemon2.apply_poison()
                        player1_poison_pots -= 1
                        display_action_result(player1_name, action1, pokemon1, pokemon2)
                    else:
                        print(f"{pokemon1.name} cannot use poison anymore!")
                    break
                else:
                    print("You don't have any Poison Pots left! Please choose another action.")
            elif action1 == "v":
                if player1_healing_pots > 0:
                    if not pokemon1.heal_used:
                        pokemon1.heal()
                        player1_healing_pots -= 1  # Decrement healing pot count
                        display_action_result(player1_name, action1, pokemon1, pokemon2)
                    else:
                        print(f"{pokemon1.name} cannot heal anymore!")
                    break
                else:
                    print("You don't have any Healing Pots left! Please choose another action.")
            elif action1 == "b":
                pokemon1 = queue_mode(player1_name, pokemon1, player1_pokemons, pokemon2)
                display_action_result(player1_name, action1, pokemon1, pokemon2)
            else:
                print("Invalid action! Please choose again.")

        if not pokemon2.is_alive():
            fight_results.append((player1_name, pokemon1.name, pokemon2.name, "P1"))
            if all(not p.is_alive() for p in player2_pokemons):
                print_centered_header("Champion")
                result_data = [[f"{player1_name} wins the game!"]]
                print(tabulate(result_data, tablefmt="grid", stralign="center"))
                break
            else:
                pokemon2 = queue_mode(player2_name, pokemon2, player2_pokemons, pokemon1)

        # Player 2's turn
        while True:
            display_battle_status(pokemon2, player2_name, player2_poison_pots, player2_healing_pots)
            action2 = input("Choose Action: ").strip().lower()

            if action2 == "z":
                damage, multiplier = pokemon2.calculate_damage(pokemon1)
                pokemon1.take_damage(damage)
                display_action_result(player2_name, action2, pokemon2, pokemon1, damage, multiplier=multiplier)
                break
            elif action2 == "x":
                pokemon2.is_defending = True
                pokemon2.defense_turns = 0  # Reset defense turns
                display_action_result(player2_name, action2, pokemon2, pokemon1)
                break
            elif action2 == "c":
                if player2_poison_pots > 0:
                    if not pokemon2.poisoned and pokemon2.poison_turns < 3:
                        pokemon1.apply_poison()
                        player2_poison_pots -= 1
                        display_action_result(player2_name, action2, pokemon2, pokemon1)
                    else:
                        print(f"{pokemon2.name} cannot use poison anymore!")
                    break
                else:
                    print("You don't have any Poison Pots left! Please choose another action.")
            elif action2 == "v":
                if player2_healing_pots > 0:
                    if not pokemon2.heal_used:
                        pokemon2.heal()
                        player2_healing_pots -= 1  # Decrement healing pot count
                        display_action_result(player2_name, action2, pokemon2, pokemon1)
                    else:
                        print(f"{pokemon2.name} cannot heal anymore!")
                    break
                else:
                    print("You don't have any Healing Pots left! Please choose another action.")
            elif action2 == "b":
                pokemon2 = queue_mode(player2_name, pokemon2, player2_pokemons, pokemon1)
                display_action_result(player2_name, action2, pokemon2, pokemon1)
            else:
                print("Invalid action! Please choose again.")

        if not pokemon1.is_alive():
            fight_results.append((player2_name, pokemon2.name, pokemon1.name, "P2"))
            if all(not p.is_alive() for p in player1_pokemons):
                print_centered_header("Champion")
                result_data = [[f"{player2_name} wins the game!"]]
                print(tabulate(result_data, tablefmt="grid", stralign="center"))
                break
            else:
                pokemon1 = queue_mode(player1_name, pokemon1, player1_pokemons, pokemon2)

        # Apply poison damage at the end of each turn
        pokemon1.take_poison_damage()
        pokemon2.take_poison_damage()

    # Print the results of each fight
    display_battle_results(fight_results)

def choose_pokemons(pokemons, player_name, previous_pokemons=None):
    chosen_pokemons = []
    print(f"\n{player_name}, choose your 3 Pokémon (e.g., '1 2 3'):")

    while len(chosen_pokemons) < 3:
        # Prepare data
        table_data = [[i + 1, pokemon.name, "/".join(pokemon.types)] for i, pokemon in enumerate(pokemons)]
        print(tabulate(table_data, headers=["No", "Name", "Type"], tablefmt="grid", stralign="center"))

        choices = input(f"Choose Pokémon: ").split()
        for choice in choices:

            try:
                index = int(choice) - 1
                if 0 <= index < len(pokemons) and pokemons[index] not in chosen_pokemons:
                    chosen_pokemons.append(pokemons.pop(index))
                else:
                    print(f"Invalid choice or Pokémon already chosen: {choice}. Try again.")
            except ValueError:
                print(f"Invalid input: {choice}. Please enter numbers only.")

        if len(chosen_pokemons) > 3:
            print("You can only choose 3 Pokémon. Please try again.")
            chosen_pokemons = chosen_pokemons[:3]  # Limit to 3 Pokémon

    return chosen_pokemons

def coin_flip():
    print("\nCoin Flip to Determine Who Chooses First!")
    player1_choice = input("Player 1, choose H for Heads or T for Tails: ").strip().lower()
    player2_choice = input("Player 2, choose H for Heads or T for Tails: ").strip().lower()

    # Convert single letters to full words
    choice_map = {'h': 'heads', 't': 'tails'}

    if player1_choice not in ['h', 't'] or player2_choice not in ['h', 't']:
        print("Invalid choice! Please choose either 'H' for Heads or 'T' for Tails.")
        return coin_flip()  # Restart the coin flip if invalid input

    # Convert choices to full words for internal logic
    player1_choice = choice_map[player1_choice]
    player2_choice = choice_map[player2_choice]

    flip_result = random.choice(['heads', 'tails'])
    print(f"\nThe coin landed on: {flip_result}")

    if flip_result == player1_choice:
        print("Player 1 wins the coin flip! Player 1 chooses first.")
        return 1  # Player 1 chooses first
    else:
        print("Player 2 wins the coin flip! Player 2 chooses first.")
        return 2  # Player 2 chooses first

def choose_pokemon_for_battle(player_name, pokemons):
    display_queue(player_name, pokemons)
    while True:
        try:
            choice = int(input(f"{player_name}, choose the Pokémon to fight (1-{len(pokemons)}): ")) - 1
            if 0 <= choice < len(pokemons) and pokemons[choice].is_alive():
                return pokemons[choice]
            else:
                print("Invalid choice or Pokémon is fainted. Please choose again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Define Pokémon with types, strengths, and weaknesses
    all_pokemons = [
        Pokemon("Snorlax", ["Normal"], [], ["Fighting"]),
        Pokemon("Charizard", ["Fire", "Flying"], ["Grass", "Bug", "Ice", "Steel"], ["Water", "Electric", "Rock"]),
        Pokemon("Gyarados", ["Water", "Flying"], ["Fire", "Ground", "Rock"], ["Electric", "Rock"]),
        Pokemon("Venusaur", ["Grass", "Poison"], ["Water", "Ground", "Rock"], ["Fire", "Ice", "Flying", "Psychic"]),
        Pokemon("Pikachu", ["Electric"], ["Water", "Flying"], ["Ground"]),
        Pokemon("Lapras", ["Water", "Ice"], ["Grass", "Ground", "Flying", "Dragon"], ["Electric", "Fighting", "Rock", "Steel"]),
        Pokemon("Machamp", ["Fighting"], ["Normal", "Ice", "Rock", "Dark", "Steel"], ["Flying", "Psychic", "Fairy"]),
        Pokemon("Gengar", ["Ghost", "Poison"], ["Grass", "Fairy"], ["Psychic", "Dark", "Ghost"]),
        Pokemon("Groudon", ["Ground"], ["Fire", "Electric", "Poison", "Rock", "Steel"], ["Water", "Grass", "Ice"]),
        Pokemon("Rayquaza", ["Dragon", "Flying"], ["Grass", "Fighting", "Bug"], ["Ice", "Rock", "Dragon", "Fairy"]),
        Pokemon("Mewtwo", ["Psychic"], ["Fighting", "Poison"], ["Bug", "Ghost", "Dark"]),
        Pokemon("Scizor", ["Bug", "Steel"], ["Grass", "Psychic", "Dark"], ["Fire"]),
        Pokemon("Tyranitar", ["Rock", "Dark"], ["Fire", "Ice", "Flying", "Bug"], ["Water", "Grass", "Fighting", "Ground", "Fairy"]),
        Pokemon("Dragonite", ["Dragon", "Flying"], ["Dragon"], ["Ice", "Dragon", "Fairy"]),
        Pokemon("Umbreon", ["Dark"], ["Psychic", "Ghost"], ["Fighting", "Bug", "Fairy"]),
        Pokemon("Metagross", ["Steel", "Psychic"], ["Ice", "Rock", "Fairy"], ["Fire", "Ground", "Dark"]),
        Pokemon("Sylveon", ["Fairy"], ["Fighting", "Dragon", "Dark"], ["Poison", "Steel"])
    ]

    print_centered_header("Pokémon Battle")
    
    # Create a fresh copy of the Pokémon list for each round
    pokemons = [Pokemon(pokemon.name, pokemon.types, pokemon.strong_against, pokemon.weak_against) for pokemon in all_pokemons]

    # Play Coin Flip to determine who chooses first
    first_player = coin_flip()

    # Players choose Pokémon
    if first_player == 1:
        player1_pokemons = choose_pokemons(pokemons, "Player 1")
        player2_pokemons = choose_pokemons(pokemons, "Player 2", player1_pokemons)
    else:
        player2_pokemons = choose_pokemons(pokemons, "Player 2")
        player1_pokemons = choose_pokemons(pokemons, "Player 1", player2_pokemons)

    # Display queue and choose Pokémon for battle
    p1_active = choose_pokemon_for_battle("Player 1", player1_pokemons)
    p2_active = choose_pokemon_for_battle("Player 2", player2_pokemons)

    # Battle the chosen Pokémon
    battle(p1_active, p2_active, "Player 1", "Player 2", player1_pokemons, player2_pokemons)

if __name__ == "__main__":
    main()
