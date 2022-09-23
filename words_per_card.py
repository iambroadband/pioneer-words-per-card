import os
from recordclass import dataobject
import scrython
from typing import List


class Deck(dataobject):
    name: str
    size: int
    total_words: int
    average_words_per_card: int


def word_count(card: scrython.cards.named.Named) -> int:
    # Non-MDFC
    try:
        return len(card.oracle_text().split(" "))
    # MDFC
    except KeyError:
        return sum([len(face["oracle_text"].split(" ")) for face in card.card_faces()])


def main():
    deck_dir = "./decks"
    decks: List[Deck] = []

    for filename in os.scandir(deck_dir):
        if filename.is_file():
            # print(filename.path)
            with open(filename.path) as deck_file:
                deck = Deck(
                    name=os.path.basename(filename.path).split(".")[0],
                    size=0,
                    total_words=0,
                    average_words_per_card=0,
                )

                for line in deck_file:
                    if not line.isspace():
                        # print(line)
                        (quantity, card_name) = line.split(" ", 1)
                        quantity = int(quantity)
                        card = scrython.cards.Named(fuzzy=card_name)
                        line_words = quantity * word_count(card)

                        deck.size += quantity
                        deck.total_words += line_words

                deck.average_words_per_card = deck.total_words / deck.size
                decks.append(deck)

    for deck in sorted(decks, key=lambda d: d.average_words_per_card, reverse=True):
        print(deck)


if __name__ == "__main__":
    main()
