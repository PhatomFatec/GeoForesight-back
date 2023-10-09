### Execution Installation Guide

#### First, some prerequisites:

**To run this project locally, you will need:**

* The latest version of PostgreSQL installed on your machine, which is currently version 15. Follow the [installation guide](https://www.2ndquadrant.com/en/blog/pginstaller-install-postgresql/).
* Install the extension that we are using to see plots, install postgis by following the [link](https://postgis.net/documentation/getting_started/install_windows/)
* After that, access the database path, and execute the database creation, which can be found in this repository in the **create.sql** file.
* Then, execute the data insertion into the database, which can be found in this repository in the **insert_postgres** folder that contains all the insertion functions.
* You need to have Python installed on your machine. In this project, we developed using version 3.8.10. Follow the [installation guide](https://wiki.python.org/moin/BeginnersGuide/Download).
* Open the command prompt on your machine, in the root path of the project, and run the following command to prepare your environment:

```
pip install -r requirements.txt
```

#### With all the previous steps done, you can finnally execute the project, running the following code, inside of **myapp** path:

```
Flask run
```
