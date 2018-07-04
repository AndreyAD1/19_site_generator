import os
import json
from jinja2 import Environment, FileSystemLoader
from jinja2_markdown import MarkdownExtension
from livereload import Server


def load_article_info():
    try:
        with open('config.json', 'r', encoding='utf-8') as json_file:
            article_info = json.load(json_file)
        return article_info
    except FileNotFoundError:
        return None


def get_html_filepath(article_info):
    for article in article_info['articles']:
        article_file_path = article['source']
        head, tail = os.path.split(article_file_path)
        file_name, extension = tail.split('.')
        html_file_path = '{}.html'.format(file_name)
        article['html_filepath'] = html_file_path
    return article_info


def get_article_context(article_dict):
    article_file_path = 'articles/{}'.format(article_dict['source'])
    with open(article_file_path) as article_file:
        article_content = article_file.read()
    article_dict['article_content'] = article_content
    return article_dict


def render_main_page(article_info, jinja_environment):
    article_info['page_title'] = 'Main page'
    index_template = jinja_environment.get_template('index.html')
    index_html = index_template.render(article_info)
    with open('static/index.html', 'w', encoding='utf-8') as index_file:
        index_file.write(index_html)


def render_article_pages(article_info, jinja_environment):
    for article in article_info['articles']:
        article_context = get_article_context(article)
        article_template = jinja_environment.get_template('_article.html')
        article_html = article_template.render(article_context)
        article_filepath = 'static/{}'.format(article['html_filepath'])
        with open(article_filepath, 'w', encoding='utf-8') as article_file:
            article_file.write(article_html)


def render_site():
    article_json = load_article_info()
    if article_json is None:
        exit('Can not find "config.json" file.')
    article_json = get_html_filepath(article_json)
    env = Environment(
        loader=FileSystemLoader('templates/'),
        extensions=[MarkdownExtension]
    )
    render_main_page(article_json, env)
    render_article_pages(article_json, env)


if __name__ == '__main__':
    server = Server()
    server.watch('templates/', render_site)
    server.watch('articles/', render_site)
    server.watch('static/css', render_site)
    server.serve(root='static/')
