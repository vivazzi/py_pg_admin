# Ease pgAdmin installation

py_pg_admin is package for ease of pgAdmin installation with the creation of a short terminal command and icon.


## Installing

1. Open terminal and clone repo anywhere at your home folder.
   ```shell
   git clone https://github.com/vivazzi/py_pg_admin.git
   cd py_pg_admin
   ```

2. (Optional) Copy local_settings_sample.py to local_settings.py and 
   set wished parameters (using your favorite editor). To look available saved pipfiles, input:
   ```shell
   python3 pre_install.py --help
   ```

3. Run pre-installation and follow instructions:
   ```shell
   python3 pre_install.py
   ```

   This command create `.venv` folder in projects folder to virtual environment will be near with project. 
   Also command will try to add `Pipfile` specified in `local_settings.py`, if you did not add `Pipfile` yourself.
   

4. Make sure you have `pipenv >= 2020.11.15` (older version may miss required packages). 
   Check your Pipfile (create your own `Pipfile`, if you want to use other pgAdmin) and install packages:
   ```shell
   pipenv sync
   ```

5. Run in terminal:
   ```shell
   sudo python3 post_install.py
   ```

Now you can run pgAdmin in terminal `pgAdmin[major version]`, for example:
```shell
pgAdmin4
```

For convenience, you can use icon in Linux menu in Development section. 
After running icon terminal is will be opened with next instruction like this:
```shell
Starting pgAdmin 4. Please navigate to http://127.0.0.1:5050 in your browser.
 * Serving Flask app "pgadmin" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
```

And you can open pgAdmin page http://127.0.0.1:5050 in your browser. 


# CONTRIBUTING

To reporting bugs or suggest improvements, please use the [issue tracker](https://github.com/vivazzi/py_pg_admin/issues).

Thank you very much, that you would like to contribute to py_pg_admin. Thanks to the [present, past and future contributors](https://github.com/vivazzi/py_pg_admin/contributors).

If you think you have discovered a security issue in our code, please do not create issue or raise it in any public forum until we have had a chance to deal with it.
**For security issues use security@vuspace.pro**


# LINKS

- Project's home: https://github.com/vivazzi/py_pg_admin
- Report bugs and suggest improvements: https://github.com/vivazzi/py_pg_admin/issues
- Author's site, Artem Maltsev: https://vivazzi.pro
    
# LICENCE

Copyright © 2021 Artem Maltsev and contributors.

MIT licensed.