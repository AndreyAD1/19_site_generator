from staticjinja import make_site
from livereload import Server
import os
from jinja2_markdown import MarkdownExtension


def get_directories_and_article_files():
    file_dict = {}
    first_step = 0
    for step_num, file_info in enumerate(os.walk('static/articles')):
        if step_num == first_step:
            continue
        dirpath, dirnames, filenames = file_info
        directory_name = os.path.basename(dirpath)
        file_dict[directory_name] = filenames
    return file_dict


def sort_by_number(entry_name):
    splitted_filename = entry_name.split('_', maxsplit=1)
    first_splitted_item = splitted_filename[0]
    try:
        file_num = int(first_splitted_item)
        return file_num
    except ValueError:
        return entry_name


def get_article_list(folders_and_files):
    article_list = []
    for folder in sorted(folders_and_files, key=lambda x: sort_by_number(x)):
        article_group = {}
        article_group['group_name'] = folder
        article_group['article_list'] = []
        for file_name in sorted(
            folders_and_files[folder],
            key=lambda x: sort_by_number(x)
        ):
            article = {}
            file_root, file_extension = os.path.splitext(file_name)
            article['article_name'] = file_root
            article['article_html'] = '{}.html'.format(file_root)
            article_group['article_list'].append(article)
        article_list.append(article_group)
    return article_list


def get_article_content(template):
    head, tail = os.path.split(template.name)
    article_title, _ = tail.split('.')
    with open(template.filename) as template_file:
        return {
            'article': template_file.read(),
            'article_title': article_title
        }


def render_article(env, template, **kwargs):
    article_template = env.get_template('_article.html')
    head, tail = os.path.split(template.name)
    article_title, _ = tail.split('.')
    output_file_name = 'static/{}.html'.format(article_title)
    article_template.stream(**kwargs).dump(output_file_name)


def render_site():
    directories_and_files = get_directories_and_article_files()
    article_groups = get_article_list(directories_and_files)
    context_index = {
        'page_name': 'Main page',
        'article_groups': article_groups
    }
    site = make_site(
        extensions=[MarkdownExtension],
        contexts=[
            ('index.html', context_index),
            ('.*.md', get_article_content)
        ], rules=[('.*.md', render_article)],
        outpath='static/',
        searchpath='templates/'
    )
    site.render()


if __name__ == '__main__':
    render_site()
    # server = Server()
    # server.watch('templates/', func=render_site())
    # # TODO watch for changes in markdown articles
    # server.serve(root='static/')


# with open('articles/0_tutorial/7_codenvy.md') as file:
#     file_content = file.read()
#
# print(file_content)
# print(type(file_content))