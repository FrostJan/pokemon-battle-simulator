import random

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.hp = random.uniform(30, 40)  # HP between 30 and 40
        self.power = random.randint(7, 10)  # Attack power between 7 and 10
        self.is_defending = False
        self.poisoned = False
        self.poison_damage = 0
        self.poison_turns = 0
        self.heal_used = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        if self.is_defending:
            damage *= 0.9  # Reduce damage by 10% if defending
            self.is_defending = False  # Reset defense after taking damage
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self):
        if not self.heal_used:
            self.hp += 20  # Heal by 20 HP
            if self.hp > 50:  # Assuming max HP is 50
                self.hp = 50
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
        fatigue_amount = self.hp * 0.02  # 2% fatigue
        self.take_damage(fatigue_amount)

def battle(pokemon1, pokemon2):
    print(f"\nBattle: {pokemon1.name} (HP: {pokemon1.hp:.2f}) vs {pokemon2.name} (HP: {pokemon2.hp:.2f})")
    
    while pokemon1.is_alive() and pokemon2.is_alive():
        # Player 1's turn
        print(f"\n{pokemon1.name}'s turn:")
        action1 = input("Choose action (Z: Attack, X: Defense, C: Poison, V: Heal): ").strip().lower()
        
        if action1 == "z":
            print(f"{pokemon1.name} attacks {pokemon2.name}!")
            pokemon2.take_damage(pokemon1.power)
            print(f"{pokemon2.name} takes {pokemon1.power} damage! (HP: {pokemon2.hp:.2f})")
        elif action1 == "x":
            print(f"{pokemon1.name} is defending!")
            pokemon1.is_defending = True
            continue  # Skip to the next turn
        elif action1 == "c":
            if not pokemon1.poisoned and pokemon1.poison_turns < 2:
                print(f"{pokemon1.name} poisons {pokemon2.name}!")
                pokemon2.apply_poison()
                print(f"{pokemon2.name} is now poisoned! (Poison damage: {pokemon2.poison_damage:.2f})")
            else:
                print(f"{pokemon1.name} cannot use poison anymore!")
            continue  # Skip to the next turn
        elif action1 == "v":
            if not pokemon1.heal_used:
                print(f"{pokemon1.name} heals!")
                pokemon1.heal()
                print(f"{pokemon1.name} heals for 20 HP! (HP: {pokemon1.hp:.2f})")
            else:
                print(f"{pokemon1.name} cannot heal anymore!")
            continue  # Skip to the next turn
        else:
            print("Invalid action! Please choose again.")
            continue  # Skip to the next turn

        # Check if Pokémon 2 is still alive
        if not pokemon2.is_alive():
            print(f"{pokemon2.name} has fainted!")
            break

        # Player 2's turn
        print(f"\n{pokemon2.name}'s turn:")
        action2 = input("Choose action (Z: Attack, X: Defense, C: Poison, V: Heal): ").strip().lower()
        
        if action2 == "z":
            print(f"{pokemon2.name} attacks {pokemon1.name}!")
            pokemon1.take_damage(pokemon2.power)
            print(f"{pokemon1.name} takes {pokemon2.power} damage! (HP: {pokemon1.hp:.2f})")
        elif action2 == "x":
            print(f"{pokemon2.name} is defending!")
            pokemon2.is_defending = True
            continue  # Skip to the next turn
        elif action2 == "c":
            if not pokemon2.poisoned and pokemon2.poison_turns < 2:
                print(f"{pokemon2.name} poisons {pokemon1.name}!")
                pokemon1.apply_poison()
                print(f"{pokemon1.name} is now poisoned! (Poison damage: {pokemon1.poison_damage:.2f})")
            else:
                print(f"{pokemon2.name} cannot use poison anymore!")
            continue  # Skip to the next turn
        elif action2 == "v":
            if not pokemon2.heal_used:
                print(f"{pokemon2.name} heals!")
                pokemon2.heal()
                print(f"{pokemon2.name} heals for 20 HP! (HP: {pokemon2.hp:.2f})")
            else:
                print(f"{pokemon2.name} cannot heal anymore!")
            continue  # Skip to the next turn
        else:
            print("Invalid action! Please choose again.")
            continue  # Skip to the next turn

        # Check if Pokémon 1 is still alive
        if not pokemon1.is_alive():
            print(f"{pokemon1.name} has fainted!")

        # Apply poison damage at the end of each turn
        pokemon1.take_poison_damage()
        pokemon2.take_poison_damage()

        # Both Pokémon lose 2% health due to fatigue
        pokemon1.fatigue()
        pokemon2.fatigue()

def choose_pokemons(pokemons, player_name):
    chosen_pokemons = []
    print(f"\n{player_name}, choose your 3 Pokémon (e.g., '1 2 3'):")
    while len(chosen_pokemons) < 3:
        for i, pokemon in enumerate(pokemons):
            print(f"{i + 1}. {pokemon.name}")

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
    player1_choice = input("Player 1, choose Heads or Tails: ").strip().lower()
    player2_choice = input("Player 2, choose Heads or Tails: ").strip().lower()

    if player1_choice not in ['heads', 'tails'] or player2_choice not in ['heads', 'tails']:
        print("Invalid choice! Please choose either 'Heads' or 'Tails'.")
        return coin_flip()  # Restart the coin flip if invalid input

    flip_result = random.choice(['heads', 'tails'])
    print(f"\nThe coin landed on: {flip_result}")

    if flip_result == player1_choice:
        print("Player 1 wins the coin flip! Player 1 chooses first.")
        return 1  # Player 1 chooses first
    else:
        print("Player 2 wins the coin flip! Player 2 chooses first.")
        return 2  # Player 2 chooses first

def main():
    # Define Pokémon
    all_pokemons = [
        Pokemon("Pikachu"),
        Pokemon("Charmander"),
        Pokemon("Bulbasaur"),
        Pokemon("Squirtle"),
        Pokemon("Jigglypuff"),
        Pokemon("Meowth"),
        Pokemon("Eevee"),
        Pokemon("Snorlax"),
        Pokemon("Gengar"),
        Pokemon("Dragonite"),
        Pokemon("Vulpix"),
        Pokemon("Machop"),
        Pokemon("Psyduck"),
        Pokemon("Poliwag"),
        Pokemon("Abra"),
        Pokemon("Tentacool"),
        Pokemon("Geodude"),
        Pokemon("Magnemite"),
        Pokemon("Doduo"),
        Pokemon("Seel")
    ]

    player1_wins = 0
    player2_wins = 0
    rounds = 3

    for round_number in range(1, rounds + 1):
        print(f"\n--- Round {round_number} ---")
        
        # Create a fresh copy of the Pokémon list for each round
        pokemons = [Pokemon(pokemon.name) for pokemon in all_pokemons]

        # Play Coin Flip to determine who chooses first
        first_player = coin_flip()

        # Players choose Pokémon
        if first_player == 1:
            player1_pokemons = choose_pokemons(pokemons, "Player 1")
            player2_pokemons = choose_pokemons(pokemons, "Player 2")
        else:
            player2_pokemons = choose_pokemons(pokemons, "Player 2")
            player1_pokemons = choose_pokemons(pokemons, "Player 1")

        # Randomly pair up Pokémon from both players
        random.shuffle(player1_pokemons)
        random.shuffle(player2_pokemons)

        # Battle each pair of Pokémon
        for p1, p2 in zip(player1_pokemons, player2_pokemons):
            battle(p1, p2)

        # Determine winner based on remaining Pokémon
        player1_alive = sum(p.is_alive() for p in player1_pokemons)
        player2_alive = sum(p.is_alive() for p in player2_pokemons)

        if player1_alive > player2_alive:
            print("Player 1 wins this round!")
            player1_wins += 1
        elif player2_alive > player1_alive:
            print("Player 2 wins this round!")
            player2_wins += 1
        else:
            print("This round is a tie!")

    # Output statistics after three rounds
    print("\n--- Final Statistics ---")
    print(f"Player 1 Wins: {player1_wins}")
    print(f"Player 2 Wins: {player2_wins}")

    if player1_wins > player2_wins:
        print("Overall Winner: Player 1!")
    elif player2_wins > player1_wins:
        print("Overall Winner: Player 2!")
    else:
        print("Overall Result: It's a tie!")

if __name__ == "__main__":
    main()