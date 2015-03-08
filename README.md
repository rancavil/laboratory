Scraping Stackowrflow
=====================

This is an example that show how make web scraping and how use regular expressions with Python and programming 
just for fun ;-).

The application read the HTML from stackoverflow.com, searches with the regular expressions patterns, and generates an json 
representation.

     {
         "answers": 0,
         "id_question": "28918821",
         "question": "Flask - SQLAlchemy - clear tables while maintaining many-to-many linking table",
         "tags": [
             "python",
             "database",
             "flask",
             "sqlalchemy",
             "cascade"
         ],
         "timestamp": "2015-03-07 17:30:41.251444",
         "views": 5,
         "votes": 2
     }

To use it.

Clone the repository on your computer.

      $ git clone https://github.com/rancavil/laboratory.git

Go to the directory.

      $ cd laboratory/scraping

And execute.

      $ ./scraping_stackoverflow.py

Or.

      $ python scraping_stackoverflow.py
