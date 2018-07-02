from staticjinja import make_site
from livereload import Server
import os
from jinja2_markdown import MarkdownExtension
import json


def load_article_info():
    with open('config.json', 'r', encoding='utf-8') as json_file:
        article_info = json.load(json_file)
    return article_info


def get_context_index(article_info):
    article_info['page_title'] = 'Main page'
    for article in article_info['articles']:
        article_file_path = article['source']
        head, tail = os.path.split(article_file_path)
        file_name, extension = tail.split('.')
        html_file_path = '{}.html'.format(file_name)
        article['html_file'] = html_file_path
    return article_info


def get_article_content(template):
    head, tail = os.path.split(template.name)
    article_title, _ = tail.split('.')
    with open(template.filename) as template_file:
        return {
            'article_content': template_file.read(),
            'article_title': article_title
        }


def render_article(env, template, **kwargs):
    article_template = env.get_template('_article.html')
    head, tail = os.path.split(template.name)
    article_title, _ = tail.split('.')
    output_file_name = 'static/{}.html'.format(article_title)
    article_template.stream(**kwargs).dump(output_file_name)


def render_site():
    article_json = load_article_info()
    context_index = get_context_index(article_json)
    print(context_index)
    site = make_site(
        extensions=[MarkdownExtension],
        contexts=[
            ('index.html', context_index),
            ('.*.md', get_article_content)
        ],
        rules=[('.*.md', render_article)],
        outpath='static/',
        searchpath='templates/'
    )
    site.render()


if __name__ == '__main__':
    render_site()
    # server = Server()
    # server.watch('templates/', render_site)
    # # TODO watch for changes in markdown articles
    # server.serve(root='static/')
