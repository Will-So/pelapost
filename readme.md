# Pelican Auto Post
This CLI allows posting Ipython notebooks to your Pelican-powered blog.

# Example
./pelican_auto_post.py --tags *Nix --tags CLI  --title sqlite3
Enter the full notebook path: /Users/Will/Devel/blog_posts/sqlite3_CLI.ipynb

# publish.sh
This is a very short bash script that runs the necessary Pelican and github commands to publish the file to the website. 

Python must have permission to write to the content directory in the pelican blog. 
It also must have permission to execute the shell script. Both of these can be accomplished with chmod 777 pelican_dir



# TODO

- Make a one time configuration option to set the default blog directory without changing the code


# Testing
To run the tests, you need to make sure that python has permission to write to the test directory. 
