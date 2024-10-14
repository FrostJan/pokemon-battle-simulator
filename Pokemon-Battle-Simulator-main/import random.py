import random

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.hp = random.randint(30, 40)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

def battle(pokemon1, pokemon2):
    print(f"\nBattle: {pokemon1.name} vs {pokemon2.name}")
    while pokemon1.is_alive() and pokemon2.is_alive():
        # Simulate attack
        damage = random.randint(1, 10)
        pokemon2.take_damage(damage)
        print(f"{pokemon1.name} attacks {pokemon2.name} for {damage} damage. {pokemon2.name} HP: {pokemon2.hp}")

        if not pokemon2.is_alive():
            print(f"{pokemon2.name} has fainted!")
            break

        # Simulate counter-attack
        damage = random.randint(1, 10)
        pokemon1.take_damage(damage)
        print(f"{pokemon2.name} attacks {pokemon1.name} for {damage} damage. {pokemon1.name} HP: {pokemon1.hp}")

        if not pokemon1.is_alive():
            print(f"{pokemon1.name} has fainted!")

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

def choose_active_pokemon(pokemons, player_name):
    print(f"\n{player_name}, choose your active Pokémon:")
    for i, pokemon in enumerate(pokemons):
        print(f"{i + 1}. {pokemon.name} (HP: {pokemon.hp})")

    while True:
        choices = input("Choose your Pokémon: ").split()
        for choice in choices:
            try:
                index = int(choice) - 1
                if 0 <= index < len(pokemons) and pokemons[index].is_alive():
                    return pokemons[index]
                else:
                    print(f"Invalid choice or Pokémon has fainted: {choice}. Try again.")
            except ValueError:
                print(f"Invalid input: {choice}. Please enter numbers only.")

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
    pokemons = [
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

    # Play Coin Flip to determine who chooses first
    first_player = coin_flip()

    # Players choose Pokémon
    if first_player == 1:
        player1_pokemons = choose_pokemons(pokemons, "Player 1")
        player2_pokemons = choose_pokemons(pokemons, "Player 2")
    else:
        player2_pokemons = choose_pokemons(pokemons, "Player 2")
        player1_pokemons = choose_pokemons(pokemons, "Player 1")

    # Battle until one player has no Pokémon left
    while player1_pokemons and player2_pokemons:
        # Player 1 chooses active Pokémon
        active_pokemon1 = choose_active_pokemon(player1_pokemons, "Player 1")
        # Player 2 chooses active Pokémon
        active_pokemon2 = choose_active_pokemon(player2_pokemons, "Player 2")

        # Battle between chosen Pokémon
        battle(active_pokemon1, active_pokemon2)

        # Remove fainted Pokémon from the list
        player1_pokemons = [p for p in player1_pokemons if p.is_alive()]
        player2_pokemons = [p for p in player2_pokemons if p.is_alive()]

    # Determine winner
    if player1_pokemons:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")

if __name__ == "__main__":
    main()