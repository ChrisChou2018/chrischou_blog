from app.models import models


def main():
    if not models.User.table_exists():
        models.User.create_table(safe = True)
    if not models.Ariticle.table_exists():
        models.Ariticle.create_table(safe = True)
    if not models.ArticleContent.table_exists():
        models.ArticleContent.create_table(safe = True)
    print('finish...')