from staticjinja import make_site
from livereload import Server
import os


def get_article_directories():
    article_groups = []
    for entry in os.scandir('templates/articles/'):
        if not entry.name.startswith('.') and entry.is_dir():
            article_groups.append(entry)
    return article_groups


def render_site():
    context_index = {
        'page_name': 'Main page',
        'article_groups': [
            {
                'group_name': 'Арсенал',
                'article_list': [
                    {
                     'article_name': 'Гит',
                     'article_html': '#'
                    },
                    {
                     'article_name': 'Гугл',
                     'article_html': '#'
                    }
                ]
            },
            {
                'group_name': 'Арсенал',
                'article_list': [
                    {
                        'article_name': 'Гит',
                        'article_html': '#'
                    },
                    {
                        'article_name': 'Гугл',
                        'article_html': '#'
                    }
                ]
            }
        ]
    }
    site = make_site(
        contexts=[('index.html', context_index)],
        outpath='static/'
    )
    site.render()


if __name__ == '__main__':
    server = Server()
    server.watch('templates/', func=render_site())
    # TODO watch for changes in markdown articles
    server.serve(root='static/')


# with open('articles/0_tutorial/7_codenvy.md') as file:
#     file_content = file.read()
#
# print(file_content)
# print(type(file_content))