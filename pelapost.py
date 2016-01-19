#!/usr/bin/env python3
"""
Assumptions:
    1. Pelican Configuration file is pelicanconf.py
"""
# TODO make sure that replace with underscores works
# TODO Make sure that the cleanup works

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
GIT_USER_NAME = config.GIT_USER_NAME


@click.command()
@click.option('--blog-dir', default=BLOG_DIR)
@click.option('--notebook-path', prompt='Enter the full notebook path.')
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
    notebook_path = notebook_path.strip()  # Deals with case when there are trailing
    if not title:
        title = os.path.basename(notebook_path)  # extracts only the file name from the full dir
    title_no_space = re.sub('\s+', '_', title)
    make_md(blog_dir, title_no_space, tags, category)
    copy_notebook(notebook_path, blog_dir, title_no_space)
    publish(blog_dir)
    clean_notebook_path(notebook_path, title, POSTED_DIR)


def make_md(blog_dir, title, tags, category):
    """
    Makes a markdown file using the current date and other fields

    Assumptions:
        1. blog_dir/content exits. This should be the case as long as Pelican is configured
    """
    md_dir = os.path.join(blog_dir, 'content/', title +'.md')
    slug = title[:15] if len(title) > 15 else title # Truncates the title if the slug is too long

    if not os.path.exists(blog_dir):
        raise IOError("Can't find {}. Check that it exists and that it is accessible.".format(blog_dir))

    if os.path.exists(md_dir):
        raise IOError("Post with this title already exists")

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
    subprocess.call(blog_dir + 'publish.sh', GIT_USERNAME, shell=True)


def copy_notebook(notebook_path, blog_dir, title):
    """
    Moves notebook from its original location to the blog directory. Removes space.
    """
    copy_full_path = os.path.join(blog_dir, 'content/notebooks/',
                                  title + '.ipynb')

    shutil.copy(notebook_path, copy_full_path)


def clean_notebook_path(notebook_path, title, posted_dir):
    """Moves the posted notebook file into its own directory so that
    my notebook directory does not cluttered.
    """
    os.rename(notebook_path, os.path.join(notebook_path, posted_dir + title + '.ipynb'))


if __name__ == '__main__':
    _main()