Environment: python2.7 and Django 1.8.5

1. Run locally.
    Either
    (a) Using PyCharm, File->Open...->Open project directory.
        To run, Tools->Run manage.py Task, a new terminal will be opened. Type in "runserver 8000" without quotes.
        The URL is http://127.0.0.1:8000
        
    or
    (b) Using terminal, make sure python 2.7 and Django 1.8.5 are installed.
        In terminal, type "python manage.py runserver 8000"
        The URL is http://127.0.0.1:8000

2. Resources cited:
    w3school code snippets.
    http://www.maxburstein.com/blog/django-threaded-comments/
    http://www.abeautifulsite.net/whipping-file-inputs-into-shape-with-bootstrap-3/
    http://jsfiddle.net/E42XA/

3. Major files I wrote/modified this week:
    comment/
        *

    quiz/
        views.py
        templates/quiz/all_quizzes.html
        templates/quiz/quiz_page.html

        static/quiz/js/main.js

        static/quiz/css/quiz.css

    userprofile/
        templates/userprofile/*.html

    document/
        models.py
      
4. Related to testing.
    manual test plan in PDF