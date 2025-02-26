- read task.md to understand the task

# how to run
- cd to celery_mini dir
- install requirements -> pip install -r requirements.txt
- read and run dockers/init_db.md
- run api/init_app.py then open the web app and add /docs to the URL to access Swagger, which you can use for simple tests

# why elastic?
the task required to do text search over the documents, its not standard practice
to save files text in sql, I chose elastic because it indexes the text in a way that makes searching through large volumes of data very efficient
so its a good choice for situations like this where we need to search in a large amounts of data and retrieve specific results

# why sql?
I used SQL to store simple data like customer info, preferences, company details, etc. In this case categories, the data is straightforward and simple. SQL is a good choice for storing, manipulating, and retrieving this type of data, as it handles structured, lightweight data well.

# explanation of some design choices
The main focuses I had while working on this project:
- modularity
- clear and simple code
- scalability & performance

the usage of base classes, api routers, sqlAlchemy and different handlers were made to achieve those concepts

* why did I save the sum of the doc numbers in the category table?

intuitively, this should be saved in the doc data, but this would require preforming a search and sum over a lot of doc objects 
which is very slow, and there's no real reason for this as we can just query the and sum the types in sql by tracking the current sum

# major issue
the most critical issue in my opinion relates to the decision made of saving the sum in sql,
imagine going to production, two people at the same time upload a file to the same category, what will happen?
let's say the current sum is 10, now the two docs fetch this value and add their own, lets say one adds 2 and the other 3,
so we have in one hand 12, and the other 13, so both of them write their own value causing one to be overridden, this is a critical mistake as the error will exist from now on until a manual correction.

so what to do when large amount of users?

- calculate the sum in elastic? -> too slow on get request
- locking the upload? -> too slow on post request

I should research this and see how its solved in the industry but a solution that could possibly be ok is the next:
save in sql a last_updated column in category, now each time a doc is uploaded, do all the operations, return resoponse code 200 if successful, but before that, run a task that send the writing request async, you could use celery for that, 
this will be handled in a single threaded env, by using a queue.

then when some user asks for the current sum, we will get the current value in sql, and also the last update time, this value as mentioned could not be the current one, so query all the docs in elastic that have been uploaded after that, should be a relatively small number, then sum up the sql value, with the total of each of the docs in response.

this approach will ensure a smooth upload and also a correct and fast retrival of the current sum(theres still a latency of how long the data is processed in queue,
but better to have some little temporary error then a constant cumulative one, or a slow app)

# improvements in tech stack
- use docker files properly for db initialisation
- use aws s3 buckets for file storage
- use alembic for version control in the future

# possible improvements (general) and notes

- add some mock tests to ensure consistent schema and data structures
- use ids in sql(standard practice)
- I saved extra data like regions and types in elastic and sql, could be avoided, but also this data could be useful for future dev
- add certs verification in elastic, this is minimum security standard
- check for possible sql(no-sql) injection in the elastic text api, not sure if this exists but would double-check just in case
- add backups for data
- in large amounts of prod we would like to use some more advanced data engineering practice like node separation
- in elastic, I'd consider adding keyword in other indexes too
- api responses should almost always be dict to avoid future changes in response structure, this way you can just add a key in the dict, avoiding frontend unnecessary code changes 
- md5 for files, so we could double-processing the same file twice
- we could add an error config to save common error messages and codes, this would be specially great if planing on applying some translation mechanism, using lazy string _()
- we could add proper logging, save them in some elastic index

overall there are probably a lot of things that could be better, these are just some, obviously this will be terrible in large scale prod