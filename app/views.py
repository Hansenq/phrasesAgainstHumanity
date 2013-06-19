#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import app, db, models
from flask import request, render_template, redirect, url_for
import csv
import config
from factory import parse_csv_string, parse_csv_bool, get_random_phrase


@app.route('/')
@app.route('/show_cards')
def show_cards():
    white_cards = models.WhiteCard.query.all()
    black_cards = models.BlackCard.query.all()
    return render_template('show_cards.html', white_cards=white_cards,
                           black_cards=black_cards)


@app.route('/random')
def random_phrase():
    return render_template('random.html', phrase_text=get_random_phrase().text)


@app.route('/repopulate_db', methods=['GET'])
def populate_db():
    if (request.method == 'GET') & (request.args.get('import') == 'true'):
        # Deleting all tables in database
        db.drop_all()
        db.create_all()
        with open(config.SOURCE_CSV, 'rU') as csvfile:
            source_reader = csv.reader(csvfile)
            for row in source_reader:
                if row[0] == 'ID':
                    continue
                if row[8] == 'TRUE':
                    # Card is White
                    u = models.WhiteCard(
                        orig_id=row[0],
                        text=row[1],
                        in_v1=parse_csv_bool(row[5]),
                        in_v2=parse_csv_bool(row[6]),
                        watermark=parse_csv_string(row[7]),
                    )
                elif row[8] == 'FALSE':
                    # Card is Black
                    u = models.BlackCard(
                        orig_id=row[0],
                        text=row[1] + ' ',
                        num_to_draw=int(row[2]),
                        num_to_pick=int(row[3]),
                        in_v1=parse_csv_bool(row[5]),
                        in_v2=parse_csv_bool(row[6]),
                        watermark=parse_csv_string(row[7]),
                    )
                else:
                    u = models.WhiteCard(
                        orig_id='',
                        text='',
                        in_v1=bool(False),
                        in_v2=bool(False),
                        watermark=parse_csv_string(row[7]),
                    )
                db.session.add(u)
            db.session.commit()
        print 'Tables deleted and recreated. All Cards Reimported.'
    return redirect(url_for('show_cards'))
