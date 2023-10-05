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
                print(filename.path)
                if filename.path.endswith("Rakdos Midrange.txt"): # FIXME: this is a test to only use Rakdos Midrange because flip cards aren't working in scooze
                    with open(filename.path) as deck_file:
                        deck = Deck(
                            archetype=os.path.basename(filename.path).split(".")[0],
                        )

                        for line in deck_file:
                            if not line.isspace():
                                # print(line)
                                (quantity, card_name) = line.split(" ", 1)
                                quantity = int(quantity)
                                card_name = card_name.strip()
                                card = scooze.get_card_by_name(card_name)
                                deck.add_card(card, quantity)

                        decks.append(deck)

        # TODO: could sort here
        print("Deck Archetype\tTotal Words\tAverage Words")
        for deck in decks:
            print(f"{deck.archetype}\t{deck.total_words()}\t\t{deck.average_words()}")


if __name__ == "__main__":
    main()
