# Pelican Auto Post
This CLI allows posting Ipython notebooks to your Pelican-powered blog.

Note: This is not yet ready for general use.

# Example
Once installed and configured:

pelapost
>>> Enter the full notebook path:  /Users/Will/Devel/blog_posts/sqlite3_CLI.ipynb
>>> Enter the title. Must be unique: Working with SQLITE3
>>> Enter the tags: CLI 

The post will then be posted to your pelican blog automatically. 


# Installation:

## Basic Configuartion
From the main script, we need to configure

1. The `BLOG_DIR` variable. This is the directory where your website is located
2. The `AUTHOR` variable. 

# Optional Configuration: Running the Script from anywhere
It is also possible to configure your computer so we can all the script from any directory in the terminal. 
If you have never done this before, the steps are as follows:

1. Make a directory where you will store this and future CLIs. The directory I use is `~/scripts`. I also renamed this script to pac 
for convenience. 
2. Append this directory to your PYTHON_PATH. In OS X this is done by editing the `.bash_profile` file in the home directory. 
For me this is `PYTHONPATH=“:/Users/Will/Devel:/Users/Will/scripts”` 
    



# publish.sh
This is a very short bash script that runs the necessary Pelican and github commands to publish the file to the website. 

Python must have permission to write to the content directory in the pelican blog. 
It also must have permission to execute the shell script. Both of these can be accomplished with chmod 777 pelican_dir

# TODO

[ ]  Make a one time configuration option to set the default blog directory without changing the code
[ ] Test functionality one more time. Write appropriate unit tests (clean-up and tag handling)
[ ] Allow notebook path to be the current path



# Testing
To run the tests, you need to make sure that python has permission to write to the test directory.

# Troubleshooting
## [Errno 2]
There are two possible causes for this error. Depending on your OS, the script might not have write access to
your blog's directory. In this case, the solution is to use `chmod` to change the access rights.
`[Errno 2] No such file or directory: '/Users/Will/Devel/tec_blog/content/`
`chmod a+w /Users/Will/Devel/tec_blog/content/`

The second possibility is that the directory does not exist. For example, perhaps you typed in `/Users/Will/Devel/content`, forgetting
the `tech_blog` part. 