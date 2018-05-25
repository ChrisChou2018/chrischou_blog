from app.blog import views
from app.blog import account

urls = [
    (r'/login/?',           account.LoginHandlers),
    (r'/login_out/?',       account.LoginOutHandlers),
    (r'/',                  views.IndexHandlers),
    (r'/add_article/?',     views.AddArticleHandlers),
    (r'/editor_article/?',  views.EditorArticleHandlers),
    (r'/delete_article/?',  views.DeleteArticleHandler),
    (r'/article_content/?', views.ArticleContentHandlers),
]

urls += [
    (r'/j/editor_about/?',  views.JsEditorAboutHandler),
]

