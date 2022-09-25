# KU-Polls
## Online Polls And Surveys

An application for conducting online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## How to Install
1. Clone this repository
    ``` sh
    git clone https://github.com/koonwill/ku-polls.git
    ```
2. Go to ku-polls directory
    ``` sh
    cd ku-polls
    ```
3. Create Virtual Environment by:
    ``` sh
    python -m venv env
    ```
4. Start virtual environment in bash or zsh
    ``` sh
    . env/bin/activate
    ```
5. Install requirements.txt
    ``` sh
    pip install -r requirements.txt
    ```
6. Run migrations
    ``` sh
    python manage.py migrate
    ```
7. Load Dumpdata from datafixtures
    ``` sh
    python manage.py loaddata data/polls.json data/users.json
    ```
8. Follow the instructions in sample.env then create ```.env``` file name to configuration. (you can get secret key [here](https://djecrety.ir/))
## How to Run
1. Run server by (Must run in ku-polls directory.):
    ``` sh
    python manage.py runserver
    ```
2. Use this URL for application
    ``` sh
    http://127.0.0.1:8000/
    ```
## Demo Admin Username and Password
| Username  | Password  |
|-----------|-----------|
|   Admin1   | testadmin |
## Demo Username and Password
| Username  | Password  |
|-----------|-----------|
|   demo2   | 1234 |
|   demo3   | 1234 |

## Project Documents

All project documents are in the [Project Wiki](https://github.com/koonwill/ku-polls/wiki/Home).

- [Vision Statement](https://github.com/koonwill/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/koonwill/ku-polls/wiki/Requirements)
- [Iteration 1 Plan](https://github.com/koonwill/ku-polls/wiki/Iteration-1-Plan)
- [Iteration 2 Plan](https://github.com/koonwill/ku-polls/wiki/Iteration-2-Plan)
- [Iteration 3 Plan](https://github.com/koonwill/ku-polls/wiki/Iteration-3-Plan)
- [Iteration 4 Plan](https://github.com/koonwill/ku-polls/wiki/Iteration-4-Plan)
- [Development Plan](https://github.com/koonwill/ku-polls/wiki/Development-Plan)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/