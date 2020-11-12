# Python Library API Challenge by Thomas Yoo

## Goal
Create an API that will work with a rudimentary library book checkout system.

A user can do the following:
* request information about existing open book requests
* request information about a specific book request
* create a request ("take out" a book)
* delete a request ("return" a book)

Notes:
* There is no authentication so any user can delete a request


## Requirements
Python v3.6.9, with all dependencies in `requirements.txt`.
For testing, install dependencies in `requirements-dev.txt` as well.

## Set-up
I decided to use a PostgreSQL DB at the address
`postgresql+psycopg2://postgres@localhost:5432/library_api`.
This is the default location for a local DB, just named `library_api`.

Once the database is created, the initial structure can be created by running
`flask db upgrade`.

Tests are done using an automatically generated SQLite DB that is created and
destroyed upon finishing tests.

## Running the service
Navigate into the `/sample-library-api/library_api` folder.

The service can be run using `flask run` and will default to port 5000. If
desired, the argument `--port <port number>` can be appended after to specify
the port.

## Running the tests
Navigate into the `/sample-library-api/library_api` folder.

The automated tests can be run using `pytest`. This tests all necessary
functions of the endpoints.

## Structure of the service
This service has the following models:
* `Book`: representation of a book with a title
* `User`: representation of a user with an email
* `BookRequest`: representation of a request that stores the book and user IDs

The following routes can be used to manipulate `BookRequest` objects:
* `GET /request`: fetches a list of all open `BookRequest`s
* `GET /request/<int:id>`: fetches the specific `BookRequest`
* `POST /request`: accepts an `email` and `title` and returns whether or not the
book is available and the timestamp of the request
* `DELETE /request/<int:id>`: sets the `deleted_at` timestamp of the specified
`BookRequest`, effectively freeing up the book to be requested again

## Improvements to be made

For a more robust service, authentication can be added in order to limit deleting
of requests to the user who created them.

Additional endpoints for cataloguing books and users with more information can
be done as well.
