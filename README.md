# PesceMuccaBot

**Bot**, created by [Giulio Coa](https://t.me/giulioCoaInCamelCase), with the aim of reminding a friend to take supplements.

The bot will take care of sending three messages:

* one at 8.00 every morning, where he will remember to take Phosphorus and Folic Acid.
* one at 20.00 each evening, where he will remember to take iron and vitamin B12.
* one at 13.00 on the 15th of each month, where he will remember to take vitamin D.


## Modules

### Aiofile

Modules used to do asynchronous file operations

* Version: 1.5.2
* Documentation: https://github.com/mosquito/aiofile
* Modules name: **aiofile**
* Installing: `pip install --upgrade --no-cache-dir aiofile`



### APScheduler

Library that lets you schedule your Python code to be executed later, either just once or periodically

* Version: 3.6.3
* Website: https://apscheduler.readthedocs.io/en/stable/index.html
* Documentation: https://apscheduler.readthedocs.io/en/stable/modules/schedulers/asyncio.html#module-apscheduler.schedulers.asyncio
* Modules name: **apscheduler**
* Requirements:
	- Python >= 3.4: none
	- Python 3.3: **asyncio**
	- Python <= 3.2: **trollius**
* Installing: `pip install --upgrade --no-cache-dir APScheduler`



### PyMySQL

Module used to connect to a MySQL Server

* Version: 0.9.3
* Website: https://pymysql.readthedocs.io/en/latest/
* Documentation: https://pymysql.readthedocs.io/en/latest/modules/index.html
* Module name: **pymysql**
* Requirements:
	- Python -- one of the following:
		+ [CPython](http://www.python.org/) : 2.7 and >= 3.5
		+ [PyPy](http://pypy.org/) : Latest version
	- MySQL Server -- one of the following:
		+ [MySQL](http://www.mysql.com/) >= 5.5
		+ [MariaDB](https://mariadb.org/) >= 5.5
* Installing: `pip install --upgrade --no-cache-dir PyMySQL`



### Pyrogram

Module used to create the Bot

* Version: 0.17.0-async
* Website: https://docs.pyrogram.org/
* Documentation: https://docs.pyrogram.org/api/client
* Module name: **pyrogram**
* Requirements: **TgCrypto**
* Installing: `pip install --upgrade --no-cache-dir https://github.com/pyrogram/pyrogram/archive/asyncio.zip; pip install --upgrade --no-cache-dir TgCrypto`



## How to install the dependencies

To install the dependencies, create a [Virtual Enviroment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) and use: `pip install -r requirements.txt`
