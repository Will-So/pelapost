#!/usr/bin/env python3

# http://docs.getpelican.com/en/3.0/tips.html
#TODO Fix one tag problem
#TODO make sure that replace with underscores works

import click
import os
import arrow
import subprocess
import shutil

BLOG_DIR = '/Users/Will/Devel/tec_blog/'
AUTHOR = 'Will Sorenson'


@click.command()
@click.option('--blog-dir', default=BLOG_DIR)
@click.option('--notebook-path', prompt='Enter the full notebook path',
              help='files must be''located in `blog_dir`')
@click.option('--title', prompt='enter the title. Must be unique', default=None)
@click.option('--tags', prompt='enter a tag. You may enter more than one via',
              multiple=True)
@click.option('--category', default=None)
def _main(blog_dir, notebook_path, title, tags, category):
    """
    Simple program that takes the directory of a notebook
     (use `greadlink -f file.ipynb |  pbcopy`)
    and other parameters and then publishes it to my pelican blog.
    Examples
    ----
    ./pelican_auto_post.py --tags *Nix --tags CLI  --title sqlite3
    Enter the full notebook path: /Users/Will/Devel/blog_posts/sqlite3_CLI.ipynb

    """
    if not title:
        title = os.path.splitext("notebook_path")[0]  # extracts only the file name from the full dir

    make_md(blog_dir, title, tags, category)
    copy_notebook(notebook_path, blog_dir, title)
    publish(blog_dir)


def make_md(blog_dir, title, tags, category):
    """
    Makes a markdown file using the current date and other fields
    """
    md_dir = os.path.join(blog_dir, 'content/', title, '.md')

    if os.path.exists(md_dir):
        raise IOError("Post with this title already exists")

    with open(md_dir, 'w+') as post:
        post.write(("Title: {0} \n"
                    "Date: {1} \n"
                    "Category: {2}\n"
                    "Tags: {3} \n"
                    "Slug: {4} \n"
                    "Authors: {5} \n"
                    "\n"
                    "\n"
                    "{{% notebook {6}.ipynb %}}\n"
                    "        "
                    ).format(title, arrow.utcnow().date(), category, tags,
                             title.replace(" ", "_"), AUTHOR, title))


def publish(blog_dir):
    """
    Executes a bash script that processes the `contents` folder and then
    uploads that file to github.
    """
    # Just execute a bash command in the main directory here
    # http://stackoverflow.com/questions/13745648/running-bash-script-from-within-python
    # http://www.textandhubris.com/automate-pelican-with-git.html
    subprocess.call(blog_dir + 'publish.sh')


def copy_notebook(notebook_path, blog_dir, title):
    """
    Moves notebook from its original location to the
    """
    
    copy_full_path = os.path.join(blog_dir, 'content/notebooks/',
                             title.replace(' ', '_'), '.ipynb')

    shutil.copy(notebook_path, copy_full_path)


if __name__ == '__main__':
    _main()