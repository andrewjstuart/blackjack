import random
import emoji
from typing import TypedDict


class RankValue(TypedDict):
    rank: str
    value: int


class Card:
    def __init__(self, suit: str, rank: RankValue) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank["rank"]} of {self.suit}"


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []
        suits: list[str] = [
            f"Spades {emoji.emojize(":spade_suit:")}",
            f"Clubs {emoji.emojize(":club_suit:")}",
            f"Hearts {emoji.emojize(":heart_suit:")}",
            f"Diamonds {emoji.emojize(":diamond_suit:")}",
        ]
        ranks: list[RankValue] = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10},
        ]
        for suit in suits:
            # print([suit, ranks[0]])
            for rank in ranks:
                # print([suit, rank])
                # self.cards.append(([suit, rank]))
                self.cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number: int) -> list[Card]:
        cards_dealt: list[Card] = []
        for x in range(number):
            if len(self.cards) > 0:
                card: Card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self, dealer: bool = False) -> None:
        self.cards: list[Card] = []
        self.value: int = 0
        self.dealer: bool = dealer

    def add_card(self, card_list: list) -> None:
        self.cards.extend(card_list)

    def calculate_value(self) -> None:
        self.value: int = 0
        has_ace: bool = False
        for card in self.cards:
            card_value: int = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace: bool = True

        if has_ace and self.value > 21:
            self.value -= 10  # remove 10 from the total

    def get_value(self) -> int:
        self.calculate_value()
        return self.value

    def is_blackjack(self) -> int:
        return self.get_value() == 21

    def display(self, show_all_dealer_cards: bool = False) -> None:
        print(f"""{"Dealer's" if self.dealer else "Your"} hand:""")
        for index, card in enumerate(self.cards):
            if (
                index == 0
                and self.dealer
                and not show_all_dealer_cards
                and not self.is_blackjack()
            ):
                print("hidden")
            else:
                print(card)

        if not self.dealer:
            print("Value:", self.get_value())
        print()


class Game:
    dealer_wins: int = 0
    player_wins: int = 0
    game_ties: int = 0

    def play(self) -> None:
        game_number: int = 0
        games_to_play: int = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number.")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand: Hand = Hand()
            dealer_hand: Hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            if dealer_hand.is_blackjack():
                self.check_winner(
                    player_hand, dealer_hand, True
                )  # if dealer has blackjack, the game is over

            choice: str = ""
            while player_hand.get_value() <= 21 and choice not in ["s", "stand"]:
                choice: str = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice: str = input(
                        "Please enter 'Hit' or 'Stand' (or H/S)"
                    ).lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value: int = player_hand.get_value()
            dealer_hand_value: int = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final Results")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print("\n")
        print("-" * 30)
        print("Total Wins")
        print(f"Player: {Game.player_wins}")
        print(f"Dealer: {Game.dealer_wins}")
        print(f"Ties: {Game.game_ties}")
        print("-" * 30)

        print("\nThanks for playing!")

    def check_winner(
        self, player_hand: Hand, dealer_hand: Hand, game_over: bool = False
    ) -> bool:
        if not game_over:
            if player_hand.get_value() > 21:
                print(f"You busted. Dealer wins! {emoji.emojize(":frowning_face:")}")
                Game.dealer_wins += 1
                return True
            elif dealer_hand.get_value() > 21:
                print(f"Dealer busted. You win! {emoji.emojize(":grinning_face:")}")
                Game.player_wins += 1
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print(
                    f"Both players have BLACKJACK! Tie! {emoji.emojize(":neutral_face:")}"
                )
                Game.game_ties += 1
                return True
            elif player_hand.is_blackjack():
                print(f"You have BLACKJACK! You win! {emoji.emojize(":party_popper:")}")
                Game.player_wins += 1
                return True
            elif dealer_hand.is_blackjack():
                print(
                    f"Dealer has BLACKJACK! Dealer wins! {emoji.emojize(":face_with_symbols_on_mouth:")}"
                )
                Game.dealer_wins += 1
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print(f"\nYou Win! {emoji.emojize(":grinning_face:")}")
                Game.player_wins += 1
            elif player_hand.get_value() == dealer_hand.get_value():
                print(f"\nTie! {emoji.emojize(":neutral_face:")}")
                Game.game_ties += 1
            else:
                print(f"\nDealer wins. {emoji.emojize(":frowning_face:")}")
                Game.dealer_wins += 1

        return False


g: Game = Game()
g.play()

# shuffle()
# cards_dealt = deal(2)
# card = cards_dealt[0]
# rank = card[1]
#
# if rank == "A":
#    value = 11
# elif rank in ["J", "Q", "K"]:
#    value = 10
# else:
#    value = rank
#
# rank_dict = {"rank": rank, "value": value}
# print(rank_dict["rank"], rank_dict["value"])

# card = deal(1)[0]
# print(card[1]["value"])

# deck = Deck()
# deck.shuffle()
# hand = Hand()
# hand.add_card(deck.deal(2))
# print(hand.cards[0], hand.cards[1])
# hand.display()
