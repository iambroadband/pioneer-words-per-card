import os
from typing import List

import scooze.bulkdata as bulk
from scooze.api import ScoozeApi
from scooze.catalogs import ScryfallBulkFile
from scooze.deck import Deck


DOWNLOAD_CARDS = False

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
                            card_name = card_name.strip()
                            card = scooze.get_card_by_name(card_name)
                            deck.add_card(card, quantity)

                    decks.append(deck)

        # TODO: could sort here
        print(f"{'Deck Archetype':30s}{'Total Words':30s}{'Average Words':30s}")
        for deck in decks:
            print(f"{deck.archetype:30s}{deck.total_words()}\t\t\t\t{deck.average_words():4.2f}")


if __name__ == "__main__":
    main()
