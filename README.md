# NYPClassBot

## Setup Guide
- Clone this branch
- Create your venv with Python 3.8.6 (preferably without inheriting global packages. See <a href="notes-requirements">Notes</a>)
- Once you're on your venv, run `pip install -r requirements.txt` to install the packages required
- Make sure your venv folder is excluded so that it is not added to this repo

## Notes
- When you install new packages, update `requirements.txt` by running `pip freeze > requirements.txt`
<a name="notes-requirements"></a>
- When creating your venv, don't inherit global site-packages so that packages installed on your computer globally is not installed in your venv. This ensures only necessary packages are shared in `requirements.txt`
 