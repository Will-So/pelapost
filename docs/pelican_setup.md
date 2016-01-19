# Fixing
1. Creating notebooks directory
2. chmod 755
3. Settings file
4. `brew install coreutils`
    - Install needed in order to use greadutils

# Setting up a Pelican Blog
chmod 755 publish.sh

stat -f "%OLp" publish.sh

1. Quick install
2. Create notebooks directory (should be automated. 
3. Theme install from

# Installing ghp-import
`pip install ghp-import` 

# Edit the configuration file
```
PLUGIN_PATH = '/path/to/pelican-plugins'
PLUGINS = ['assets', 'sitemap', 'gravatar' 'liquid_tags.notebook']
```

# Making a first blog post
```shell
pelican content -o output -s pelicanconf.py
ghp-import output
git push origin gh-pages:master

```

 {% if EXTRA_HEADER %}
  {{ EXTRA_HEADER }}
  {% endif %}

  EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')
  
  

