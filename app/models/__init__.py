#!/usr/bin/env python
# -*- coding: utf-8 -*-
import peewee

from app.models import models

models_file_list = [
    models,
]

def init_table():
    for models in models_file_list:
        for model in dir(models):
            model_obj = getattr(models, model)
            if isinstance(model_obj, peewee.ModelBase) and \
                not model_obj.table_exists():
                model_obj.create_table(safe=True)
    else:
        print('finish....')

