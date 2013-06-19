#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import models, db
from random import randint


def parse_csv_string(s):
    if s.strip() == 'NULL':
        return ''
    else:
        return s


def parse_csv_bool(s):
    if s.strip() == 'TRUE':
        return bool(True)
    else:
        return bool(False)


def get_random_white_card():
    return models.WhiteCard.query.get(randint(0,
                                      models.WhiteCard.query.count()))


def get_random_white_cards(n):
    white_cards = []
    used_ids = []
    for r in range(n):
        c = get_random_white_card()
        while c is None:
            c = get_random_white_card()
        if not c in used_ids:
            white_cards.append(c)
            used_ids.append(c.id)
        else:
            n = n + 1
    return white_cards


def get_random_black_card():
    return models.BlackCard.query.get(randint(0,
                                      models.BlackCard.query.count()))


def find_text(black_card, white_cards):
    """ Given a black card and the correct number of white cards, returns the
    phrase. """
    orig_phrase = black_card.text
    p = ''
    (ind, starting_ind) = (-1, 0)

    # Finds corresponding '____' in black cards and replaces them with text from
    # the white card.
    for wc in white_cards:
        ind = orig_phrase.find('____', ind + 1, len(orig_phrase))
        if ind == -1:
            ind = len(orig_phrase)
        p = p + orig_phrase[starting_ind:ind] + '<em>' + wc.text + '</em>'
        starting_ind = ind + 4
    return p + orig_phrase[starting_ind:]


def get_random_phrase():
    black_card = get_random_black_card()
    while black_card is None:
        black_card = get_random_black_card()
    white_cards = get_random_white_cards(black_card.num_to_pick)
    while white_cards is None:
        white_cards = get_random_white_cards(black_card.num_to_pick)
    phrase_text = find_text(black_card, white_cards)
    filtered_list = models.Phrase.query.filter(models.Phrase.black_card_id
            == black_card.id).filter(models.Phrase.text
                                     == phrase_text).order_by(models.Phrase.votes.asc()).all()
    print 'FL: ' + repr(filtered_list)
    if (filtered_list is not None) & (len(filtered_list) != 0):
        print 'Found existing phrase, exists %r times' % len(filtered_list)
        phrase = filtered_list.pop()
    else:
        phrase = models.Phrase(text=phrase_text)
        filled_blanks = []
        for white_card in white_cards:
            filled_blank = models.FilledBlank(blank_order=len(filled_blanks))
            white_card.filled_blanks.append(filled_blank)
            phrase.filled_blanks.append(filled_blank)
            filled_blanks.append(filled_blank)
            db.session.add(filled_blank)
        db.session.add(phrase)
        db.session.commit()
    return phrase
