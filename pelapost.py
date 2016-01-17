#!/usr/bin/env python3
"""
Assumptions:
    1. Configuration file is pelicanconf.py

Needed to Generalize:
    1. init for author, blog_dir and posted_dir

Lessons Learned:
    1. Make sure I write down exactly what title is because I just ended up changing it here.
        - title is currently the file
"""
# http://docs.getpelican.com/en/3.0/tips.html
# TODO make sure that replace with underscores works
# TODO Make sure that the cleanup works
# TODO Verify that Stripping works. It may not
# TODO Allow the notebook path to be the current path
# TODO Make the clean logic a bit nicer

import config

import click
import os
import arrow
import subprocess
import shutil
import re

BLOG_DIR = config.BLOG_DIR
AUTHOR = config.AUTHOR
POSTED_DIR = config.POSTED_DIR


@click.command()
@click.option('--blog-dir', default=BLOG_DIR)
@click.option('--notebook-path', prompt='Enter the full notebook path')
@click.option('--title', prompt='enter the title. Must be unique', default=None)
@click.option('--tags', prompt='enter a tag. Seperate tags with a space')
@click.option('--category', default=None)
def _main(blog_dir, notebook_path, title, tags, category):
    """
    Simple program that takes the directory of a notebook
     (use `greadlink -f file.ipynb |  pbcopy`)
    and other parameters and then publishes it to my pelican blog.

    :param blog_dir: string; absolute directory of the pelican blog
    :param notebook_path: string; location of the
    :param title: string; Title of the blog
    :param tags: string; tags that the blo
    :param category: category of the blog

    Examples
    ----
    ./pelapost.py --tag *Nix --tag CLI  --title sqlite3
    Enter the full notebook path: ~/Devel/blog_posts/sqlite3_CLI.ipynb

    """
    if not title:
        title = os.path.basename(notebook_path)  # extracts only the file name from the full dir

    make_md(blog_dir, title, tags, category)
    copy_notebook(notebook_path, blog_dir, title)
    publish(blog_dir)
    clean_notebook_path(notebook_path, title.replace(' ', '_'))


def make_md(blog_dir, title, tags, category):
    """
    Makes a markdown file using the current date and other fields

    Assumptions:
        1. blog_dir/content exits. This should be the case as long as Pelican is configured
    """
    md_dir = os.path.join(blog_dir, 'content/', title.replace(' ', '_') +'.md')
    slug = re.sub('\s+', '_' ,title)[:10] # Truncates the title if the slug is too long

    if not os.path.exists(blog_dir):
        raise IOError("Can't see {}. Check that it exists and that it is accessible.".format(blog_dir))

    if os.path.exists(md_dir):
        raise IOError("Post with this title already exists")

    # import pdb; pdb.set_trace()

    with open(md_dir, 'w') as post:
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
                    ).format(title, arrow.utcnow().date(), category,
                             tags.replace(' ', ', '), slug, AUTHOR, title.replace(' ', '_')))


def publish(blog_dir):
    """
    Executes a bash script that processes the `contents` folder and then
    uploads that file to github.
    """
    # http://stackoverflow.com/questions/13745648/running-bash-script-from-within-python
    # http://www.textandhubris.com/automate-pelican-with-git.html
    subprocess.call(blog_dir + 'publish.sh')


def copy_notebook(notebook_path, blog_dir, title):
    """
    Moves notebook from its original location to the blog directory. Removes space s.t.
    """
    copy_full_path = os.path.join(blog_dir, 'content/notebooks/',
                                  re.sub('\s+', '_', title) + '.ipynb')

    shutil.copy(notebook_path.strip(), copy_full_path) # strip() removes trailing space


def clean_notebook_path(notebook_path, title):
    """Moves the posted notebook file into its own directory so that
    my notebook directory does not cluttered.
    """
    os.rename(notebook_path, os.path.join(notebook_path, POSTED_DIR + title + '.ipynb'))


if __name__ == '__main__':
    _main()