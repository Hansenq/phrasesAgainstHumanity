#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
DATABASE = 'tmp/phrases.db'
REF_DATABASE = 'tmp/ref.db'
SOURCE_CSV = 'tmp/sourceCards1.csv'
DEBUG = True
SECRET_KEY = 'secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
