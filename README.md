![CI Build](https://github.com/kmsherrin/databook/workflows/Run%20Tests/badge.svg)

## Intermediate Flask project putting together a slight social network type of site focused on data and collaboration (maybe?)

This was a intermediate project for testing and learning some things that I hadn't previously completed. Some of these things are:
- In's and outs of Flask, including the ecosystem surrounding
- Inbuilt user authentication
- Creation, editing, deleting, liking, commenting of posts
- Searching of posts 
- User registration and reset of password email
- Relational database design linking persistent data components, Postgres db hosted on Elephant SQL
- Deployed and hosted on heroku 
- Can handle the upload of user profile pictures and datasets
- Data uploaded to and read from amazon S3 bucket

TODO's:
- Clean up mobile UI
- Implement an elasticsearch for the Tags and Search
- Add tests for database entries
- Clean up the templates and separate out what are components (take a more JS framework approach to improve maintainability). This would also make the different view pages much neater file wise, I really should have planned the different views from the start but oh well 🤷‍♂️
- remove bootstrap usage because I am sick of it and would rather use straight CSS (or even better Tailwind)