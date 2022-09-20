# KU-Polls
## Online Polls And Surveys

An application for conducting online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run
1. Clone this repository
    ``` sh
    git clone https://github.com/koonwill/ku-polls.git
    ```
2. Install requirements.txt
    ``` sh
    pip install -r requirements.txt
    ```
3. Follow the instructions in sample.env then create ```.env``` file name to configuration. (you can get secret key [here](https://djecrety.ir/))
4. Run server by (Must run in ku-polls directory.):
    ``` sh
    python manage.py runserver
    ```
5. Use this URL for application
    ``` sh
    http://127.0.0.1:8000/
    ```

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
- [Development Plan](https://github.com/koonwill/ku-polls/wiki/Development-Plan)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/