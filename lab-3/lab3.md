# Step 1 — Setting up the Database

First, we set up the SQLite database (sqlite3 module) to store and retrieve our data

Data in SQLite is stored in tables and columns, so we first need to create a table called posts with the necessary columns. We create a .sql file that contains SQL commands to create the cats table with a few columns. We then use this schema file to create the database.

Open a database schema file called schema.sql inside your cats_app directory:

```
nano schema.sql
```

In this schema file, you first delete the cats table if it already exists. This avoids the possibility of another table named cats existing, which might result in confusing behavior (for example, if it has different columns).

We use `CREATE TABLE` posts to create the `cats` table with the following columns: