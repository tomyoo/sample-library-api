# Python Q&A API Challenge by Thomas Yoo

## Goal
Create an API that will work with a standardized test web app.

The test taker:
* fills out basic contact information (firstname, lastname, email)
* gets assigned a unique assessment instance / session (ex. 1d4c9d2b-86d9-4813-a831-dd2bcca9fe96)
* gets assessment questions
* submits assessment answers
* Gets a confirmation when the final assessment question has been submitted

Notes:
* The assessment session is timed (counting down from 1hr)
* The assessment session can be continued from another browser window
* Some of the contents of the question (either body or answer choices) are not simply text (some are html, img, etc.)


## Requirements
Python v3.6.5, with all dependencies in `requirements.txt`.
For testing, install dependencies in `requirements-dev.txt` as well.

## Set-up
I decided to use a MySQL DB at the address
`'mysql://root@localhost:3306/library_api'`.

Once the database is created, the initial structure can be created by running
the SQL commands in `migrations/initial-migration.sql`.

## Running the service
The service can be run using `flask run` and will default to port 5000. If
desired, the argument `--port <port number>` can be appended after to specify
the port.

## Running the tests
The automated tests can be run using `pytest`. This tests all necessary
functions of the endpoints.

## Structure of the service
This service has `Question` objects that have `answers`, which are `Answer`
objects with `answer` strings.

This relationship is stored in the table `answers__questions`.

has a `User` object who is the user, which stores their `first_name`,
`last_name`, and `email`.

`User`s can open a `Session` which stores the current timestamp in
`start_time`, the `user` that started the session, and any `answers` they
chose.

This relationship is stored in the table `sessions__answers`.

## Improvements to be made

With more time, I would clean up the way that answers are returned. I couldn't
decide if it was better to return everything with IDs in order to allow the
frontend to choose how to display it, or if it was better to display the
actual text. I'm leaning towards IDs, but implemented the text to make it
more readable when directly testing the API.
