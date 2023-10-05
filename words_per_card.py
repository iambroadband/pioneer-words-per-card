import os
from typing import List

import scooze.bulkdata as bulk
import scrython
from scooze.api import ScoozeApi
from scooze.catalogs import ScryfallBulkFile
from scooze.deck import Deck

DOWNLOAD_CARDS = False


def word_count(card: scrython.cards.named.Named) -> int:
    # Non-MDFC
    try:
        return len(card.oracle_text().split(" "))
    # MDFC
    except KeyError:
        return sum([len(face["oracle_text"].split(" ")) for face in card.card_faces()])


def main():
    with ScoozeApi() as scooze:
        if DOWNLOAD_CARDS:
            bulk.download_bulk_data_file_by_type(ScryfallBulkFile.ORACLE)
            scooze.load_card_file(ScryfallBulkFile.ORACLE)

        deck_dir = "./decks"
        decks: List[Deck] = []

        for filename in os.scandir(deck_dir):
            if filename.is_file():
                # print(filename.path)
                with open(filename.path) as deck_file:
                    deck = Deck(
                        archetype=os.path.basename(filename.path).split(".")[0],
                    )

                    for line in deck_file:
                        if not line.isspace():
                            # print(line)
                            (quantity, card_name) = line.split(" ", 1)
                            quantity = int(quantity)
                            card = scooze.get_card_by_name(card_name)
                            deck.add_card(card)

                    decks.append(deck)

        for deck in sorted(decks, key=lambda d: d.average_words_per_card, reverse=True):
            print(f"{deck.archetype} - {deck.average_words()}")


if __name__ == "__main__":
    main()
