[![Build Status](https://travis-ci.org/jobiols/odoo-env.svg?branch=master)](https://travis-ci.org/jobiols/odoo-env)
[![codecov](https://codecov.io/gh/jobiols/odoo-env/branch/master/graph/badge.svg)](https://codecov.io/gh/jobiols/odoo-env)

Odooenv
=======

Warning
-------
This code is is under development (stay tuned)

Directory structure

    /odoo
    ├── odoo-9.0
    │   ├── glinsar
    │   │    ├── config             odoo.conf
    │   │    ├── data_dir           filestore
    │   │    ├── log                odoo.log
    │   │    ├── postgresql         postgres database
    │   │    └── sources            custom sources
    │   ├── extra-addons            repos from image for debug
    │   ├── dist-local-packages     packages from image for debug
    │   └── dist-packages           pagkages from image for debug
    ├── nginx
    │   ├── conf
    │   ├── log
    │   └── cert
    └── postfix


Functionality so far
--------------------- 
usage: oe.py [-h] [-i] [-c CLIENT] [-v] [--debug] [--no-repos] [-R] [-r]
             [--no-dbfilter] [-S] [-s] [-u] [-d DATABASE] [-m MODULE]

    ==========================================================================
    Odoo Environment Manager v0.2.1 - by jeo Software <jorge.obiols@gmail.com>
    ==========================================================================
    
    optional arguments:
      -h, --help            show this help message and exit
      -i, --install-cli     Install client, requires -c option. Creates dir
                            structure, Pull repos and images, and generate odoo
                            config file
      -c CLIENT             Client name.
      -v, --verbose         Go verbose mode. Prints every command
      --debug               This option has the following efects: 1.- when doing
                            an update all, (option -u) it forces debug mode. 2.-
                            When running environment (option -R) it opens port
                            5432 to access postgres server databases. 3.- when
                            doing a pull (option -p) it clones the full repo i.e.
                            does not issue --depth 1 to git
      --no-repos            Does not clone or pull repos used with -i or -p
      -R, --run-env         Run postgres and aeroo images.
      -r, --run-cli         Run client odoo, requires -c options
      --no-dbfilter         Eliminates dbfilter: The client can see any database.
                            Without this, the client can only see databases
                            starting with clientname_
      -S, --stop-env        Stop postgres and aeroo images.
      -s, --stop-cli        Stop client images, requires -c options.
      -u, --update-all      Update all requires -d -c and -m options. Use --debug
                            to force update with host sources
      -d DATABASE           Database name. Note that there is a dbfilter option by
                            default the database name must begin with clientname_
      -m MODULE             Module to update or all for updating all the
                            registered modules. You can specify multiple -m
                            options. i.e. -m all forall modules -m sales stock for
                            updating sales and stock modules
      --nginx               Add nginx to installation: With -i creates nginx dir
                            w/ sample config file. with -r starts an nginx
                            container linked to odoowith -s stops nginx
                            containcer. You must add certificates and review
                            nginx.conf file.
      -Q repo test_file, --quality-assurance repo test_file
                            Perform QA running tests, arguments are Repo where
                            test lives, and yml/py test file to run (please
                            include extension). Need -d, -m and -c options Note:
                            for the test to run there must be an admin user with
                            password admin


Tool to manage docker based odoo environments

jeo Software (c) 2018 jorge.obiols@gmail.com

This code is distributed under the AGPL license

Installation
------------
    some day : pip install docker-odoo-env
    
    for now:
    cd
    git clone https://github.com/jobiols/odoo-env.git
    sudo ./odoo-env/data/install_scripts
 
    
Changelog
---------

- 0.2.1   On QA, expose port 1984 for debug purpoes with WDB
- 0.2.0   Quality Assurance support, add script for docker install, add
        command sd rmall for removing all docker imagages in memory
- 0.1.0   Nginx support, 
        Script to install docker (in script folder, execute manually)
        sd command (short for sudo docker plus some enhacements)
- 0.0.2   minor fixes
- 0.0.1   starting version
