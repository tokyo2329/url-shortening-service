To complete this exercise, I decided to go with a simple but effective (at least I think so) method.

Every given url is given a 10 character replacing url.
The "replacing url" is randomly generated using ascii characters.

If the generated url already exists in the database, it generates it again. (although, there's a small chance of it generating the exact same copy of another one existing)

Everything is done in the "urlshortener" django app.