#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
from app import db, models, factory, app
from config import basedir


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' \
            + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_phrases_with_black_cards(self):
        b = models.BlackCard(orig_id=1, text='THIS IS A TEST ____ BLACK CARD 1'
                             , num_to_draw=1)
        w = models.WhiteCard(orig_id=1, text='this is a test white card 1',
                             watermark='watermelon')
        print b, w
        db.session.add(w)
        db.session.add(b)
        db.session.commit()
        rb = factory.get_random_black_card()
        print rb
        if rb is None:
            print 'rb is none!'
            rb = b
        p = models.Phrase()
        rb.phrases.append(p)
        rw = factory.get_random_white_card()
        if rw is None:
            print 'rw is none!'
            rw = w
        fb = models.FilledBlank()
        # Adds the filled blank to the phrase
        p.filled_blanks.append(fb)
        # Adds the filled blank to the white card
        rw.filled_blanks.append(fb)
        db.session.add(fb)
        db.session.add(p)
        db.session.commit()
        
        b2 = models.BlackCard(orig_id=1, text='THIS IS A TEST ____ BLACK CARD 2'
                              , num_to_draw=1)
        w2 = models.WhiteCard(orig_id=1, text='this is a test white card 2',
                              watermark='watermelon')
        db.session.add(w2)
        db.session.add(b2)
        db.session.commit()
        # creates the final phrase!
        # p.find_text()

        # Testing uniqueness of phrase.text.
        p2 = models.Phrase()
        db.session.add(p2)
        fb2 = models.FilledBlank()
        rw.filled_blanks.append(fb2)
        p2.filled_blanks.append(fb2)
        db.session.commit()
        rb.phrases.append(p2)
        b3 = models.BlackCard(orig_id=1, text='THIS IS A TEST ____ BLACK CARD 3'
                              , num_to_draw=1)
        w3 = models.WhiteCard(orig_id=1, text='this is a test white card 3',
                              watermark='watermelon')
        db.session.add(w3)
        db.session.add(b3)
        db.session.commit()
        # p2.find_text()
        # Doesn't have to be unique, because text is changed after the phrase is
        # added.

        print p
        phrs = rb.phrases
        for c in phrs:
            print 'reached 1'
            print c
        fblnks = rw.filled_blanks
        for fblnk in fblnks:
            print 'reached 2'
            print fblnk.phrase


if __name__ == '__main__':
    unittest.main()
