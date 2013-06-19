#!/usr/bin/python
# -*- coding: utf-8 -*-
from flaskext.sqlalchemy import before_models_committed
from app import app


@before_models_committed.connect_via(app)
def before_models_committed(sender, changes):
    for (obj, change) in changes:
        if change == 'delete' and hasattr(obj, '__before_commit_delete__'):
            obj.__before_commit_delete__()
