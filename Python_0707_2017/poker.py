#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета. Черный джокер '?B' может быть
# использован в качестве треф или пик любого ранга, красный
# джокер '?R' - в качестве черв и бубен люього ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertoolsю
# Можно свободно определять свои функции и т.п.
# -----------------
from collections import Counter
from itertools import combinations, product

RANKS = [str(num) for num in range(2, 10)] + \
        ['T', 'J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']
JOKER_REPLACEMENTS = {
    '?B': [
        ''.join(card_tuple)
        for card_tuple in product(RANKS, ('C', 'S'))
    ],
    '?R': [
        ''.join(card_tuple)
        for card_tuple in product(RANKS, ('D', 'H'))
    ]
}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return sorted(
        [RANKS.index(card[0]) for card in hand], reverse=True
    )


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return len({card[-1] for card in hand}) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return sorted(ranks) == range(min(ranks), max(ranks) + 1)


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    counter = Counter(ranks)
    matched_ranks = [
        rank for rank in counter if counter[rank] == n
    ]
    if matched_ranks:
        return max(matched_ranks)


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    first_pair = kind(2, ranks)
    if first_pair:
        second_pair = kind(
            2, [rank for rank in ranks if rank != first_pair]
        )
        if second_pair:
            return first_pair, second_pair


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    max_hand_rank, current_best_hand = (0, []), None
    for five_card_hand in combinations(hand, 5):
        current_rank = hand_rank(five_card_hand)
        if current_rank > max_hand_rank:
            max_hand_rank = current_rank
            current_best_hand = five_card_hand
    return current_best_hand


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    hands = [hand]
    new_hands = hands
    for joker in ('?B', '?R'):
        for _hand in hands:
            if joker in _hand:
                new_hands.extend([
                        _hand[:_hand.index(joker)] +
                        [joker_card] +
                        _hand[_hand.index(joker)+1:]
                        for joker_card in
                        JOKER_REPLACEMENTS[joker]
                        if joker_card not in hand
                    ])
        hands = new_hands
    hands = filter(
        lambda x: '?B' not in x and '?R' not in x,
        hands
    )
    best_hands = [best_hand(_hand) for _hand in hands]
    return max(best_hands, key=hand_rank)


def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'test_best_hand passes'
    print 'OK'


def test_best_wild_hand():
    print "test_best_wild_hand..."
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
