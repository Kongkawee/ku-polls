# Installation

## Table of Contents
- [Installation for MacOS / Linux](#installation-for-macos--linux)
- [Installation for Windows](#installation-for-windows)

### Installation for MacOS / Linux

1. Open your terminal and Clone this repository on your computer.
   ```
   git clone https://github.com/Kongkawee/ku-polls.git
   ```
   
2. Open the repository or type this in your terminal.
   ```
   cd ku-polls
   ```
   
3. Set Up virtual environment.  
   1. Create your virtual environment.
      ```
      python -m venv venv
      ```
      > Note: If you can not use `python` command, Use `python3` for the rest 
   of the instruction instead. And also `pip3` instead of `pip`.
   2. Activate the virtual environment by running:
      ```
      . venv/bin/activate 
      ```
   3. Install some requirements.
      ```
      pip install -r requirements.txt
      ```
4. Create `.env` file using the given `sample.env` file.
      ```
      cp sample.env .env
      ```
5. Follow the instructions in the `.env` file for setting up externalized variables.
6. Set-Up database and data.
   1. Run migration for set up your database.
      ```
      python manage.py migrate
      ```
   2. Load data.
      ```
      python manage.py loaddata data/polls_no_votes.json
      python manage.py loaddata data/users.json
      ```
7. Try to run tests, All test should be passes.
      ```
      python manage.py test polls
      ```
8. Run the program.
      ```
      python manage.py runserver
      ```

### Installation for Windows

1. Open your terminal or Command Prompt.
2. Clone this repository on your computer.
   ```
   git clone https://github.com/Kongkawee/ku-polls.git
   ```
3. Open the repository in your terminal.
   ```
   cd ku-polls
   ```

4. Set Up virtual environment.
   1. Create your virtual environment.
      ```
      python -m venv venv
      ```
   > Note: If you cannot use the `python` command, use `python3` 
for the rest of the instructions instead. Also, use `pip3` instead of `pip`.
   2. Activate the virtual environment by running:
      ```
      venv\Scripts\activate
      ```
   3. Install some requirements.
      ```
      pip install -r requirements.txt
      ```
5. Create a `.env` file using the provided `sample.env` file.
   ```
   copy sample.env .env
   ```
6. Follow the instructions in the `.env` file to set up externalized variables.

7. Set Up the database and data.
   1. Run migrations to set up your database.
      ```
      python manage.py migrate
      ```
   2. Load data.
      ```
      python manage.py loaddata data\polls.json
      python manage.py loaddata data\users.json
      ```
8. Try to run tests; all tests should pass.
   ```
   python manage.py test polls
   ```
9. Run the program.
   ```
   python manage.py runserver
   ```

