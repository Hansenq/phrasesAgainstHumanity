#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import db


class FilledBlank(db.Model):

    # has also white_card and phrase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    white_card_id = db.Column(db.Integer, db.ForeignKey('white_card.id'))
    phrase_id = db.Column(db.Integer, db.ForeignKey('phrase.id'))
    # Starts at 0
    blank_order = db.Column(db.Integer, default=-1)

    def __repr__(self):
        return '<Filled Blank connecting Phrase %r, WC %r' % (self.phrase_id,
                self.white_card_id)


class WhiteCard(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orig_id = db.Column(db.Integer)
    text = db.Column(db.String, unique=True)
    in_v1 = db.Column(db.Boolean, default=False)
    in_v2 = db.Column(db.Boolean, default=False)
    watermark = db.Column(db.String)
    filled_blanks = db.relationship('FilledBlank', backref='white_card',
                                    lazy='dynamic')

    def __repr__(self):
        return '<White Card: #%r (%r), %s>' % (self.id, self.orig_id, self.text)


class BlackCard(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orig_id = db.Column(db.Integer)
    text = db.Column(db.String, unique=True)
    num_to_draw = db.Column(db.Integer)
    num_to_pick = db.Column(db.Integer)
    in_v1 = db.Column(db.Boolean, default=False)
    in_v2 = db.Column(db.Boolean, default=False)
    watermark = db.Column(db.String)
    phrases = db.relationship('Phrase', backref='black_card', lazy='dynamic')

    def __repr__(self):
        return '<Black Card: #%r (%r), %s, %r, %r>' % (
            self.id,
            self.orig_id,
            self.text,
            self.num_to_draw,
            self.num_to_pick,
        )


class Phrase(db.Model):

    # has also black_card
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    votes = db.Column(db.Integer, default=0)
    text = db.Column(db.String, default='')
    black_card_id = db.Column(db.Integer, db.ForeignKey('black_card.id'))
    filled_blanks = db.relationship(
        'FilledBlank',
        backref='phrase',
        lazy='dynamic',
        order_by='FilledBlank.blank_order',
    )

    def __repr__(self):
        s = '<Phrase %r on BC %r with WCs ' % (self.id, self.black_card_id)
        # Finds corresponding '____' in black cards and replaces them with text
        # from the white card.
        for assocs in self.filled_blanks:
            s = s + str(assocs.white_card_id) + ' '
        s = s + ': %s' % self.text
        return s

    def __before_commit_delete__(self):
        for filled_blank in self.filled_blanks:
            db.session.delete(filled_blank)
