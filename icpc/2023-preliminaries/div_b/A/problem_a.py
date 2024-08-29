#!/usr/bin/env python3

# A Game of Sets
#
# https://sppcontests.org/problem_pdfs/2023/prelimsB.pdf


from typing import Iterable, List, Set


def test():
    """
    Run `pytest <this-file>`.
    """

    def remove_order(nums_list: str) -> str:
        return " ".join(map(str, sorted(map(int, nums_list.split(" ")))))

    def test_algo(algo):
        assert (
            algo(
                input="""3
two oval purple striped
one squiggle purple solid
three diamond purple empty
"""
            )
            == remove_order("1 2 3")
        )

        assert (
            algo(
                input="""3
two diamond red striped
one squiggle green solid
three diamond purple empty"""
            )
            == remove_order("0")
        )

        assert (
            algo(
                input="""5
one squiggle purple solid
two diamond red striped
one squiggle green empty
two oval purple empty
two squiggle green solid"""
            )
            == remove_order("5 2 4")
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force, solution.hashset]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Generate all pairs of 3 cards, and check if they form a valid set.
        Time:      O(n^3): Given n cards, we check all pairs of 3, of which there are n^3 on whether they form a set (O(1)).
        Space:     O(1): No additional memory is used.
        """

        def forms_set(card1, card2, card3) -> bool:
            numbers, shapes, colours, shadings = set(), set(), set(), set()
            for card in [card1, card2, card3]:
                number, shape, colour, shading = card
                numbers.add(number)
                shapes.add(shape)
                colours.add(colour)
                shadings.add(shading)

            return all(
                property_count == 3 or property_count == 1
                for property_count in map(
                    len, (numbers, shapes, colours, shadings)
                )
            )

        indexed_cards = list(
            enumerate(map(str.split, input.splitlines()[1:]), start=1)
        )

        for id1, card1 in indexed_cards:
            for id2, card2 in indexed_cards:
                for id3, card3 in indexed_cards:
                    # Skip handling same card twice.
                    if id1 == id2 or id2 == id3:
                        continue

                    if forms_set(card1, card2, card3):
                        return f"{id1} {id2} {id3}"

        return "0"

    def hashset(self, input=str) -> str:
        """
        Approach:  Calculate third required card.
        Idea:      For each pair of 2 cards, calculate the third card that would make it a valid set (this card is unique).
        Time:      O(n^2): Given n cards, for each pair of 2 cards, of which there are n^2, we calculate the third card that would make it a valid set (O(1)), and then we check if we have that card (O(1)).
        Space:     O(n): We store each card along with its id (size O(n)), and we also store a hashmap mapping card to id (size O(n)).
        """

        properties = [
            {"one", "two", "three"},
            {"diamond", "oval", "squiggle"},
            {"green", "purple", "red"},
            {"empty", "solid", "striped"},
        ]

        indexed_cards = list(
            enumerate(
                map(
                    lambda properties_list: tuple(properties_list),
                    (map(str.split, input.splitlines()[1:])),
                ),
                start=1,
            )
        )

        card_to_id = dict()
        for card_id, card in indexed_cards:
            card_to_id[card] = card_id

        def required_third_card_properties(card1, card2):
            for property_id, (property1, property2) in enumerate(
                zip(card1, card2)
            ):
                if property1 == property2:
                    # The property of the third card must be the same.
                    property3 = property1
                else:
                    # The property of the third card must be unique, so the
                    # other remaining property value.
                    property3 = next(
                        iter(properties[property_id] - {property1, property2})
                    )
                yield property3

        def required_third_card(card1, card2):
            return tuple(required_third_card_properties(card1, card2))

        n = len(indexed_cards)

        for i, (id1, card1) in ((i, indexed_cards[i]) for i in range(0, n)):
            for id2, card2 in (indexed_cards[i] for i in range(i + 1, n)):
                card3 = required_third_card(card1, card2)
                if (id3 := card_to_id.get(card3, None)) is not None:
                    return f"{id1} {id2} {id3}"

        return "0"
