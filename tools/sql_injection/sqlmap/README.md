# sqlmap

Everytime we run it again it picks up when it left of and doesn't rerun everything but uses a file for caching info

The image you provided shows a command being executed using `sqlmap`, a tool commonly used for automating SQL injection attacks. Here's a breakdown of the command:

```bash
sqlmap -r reset.req -p email --level 5 --risk 3 --technique=B
```

### Explanation:
- **sqlmap**: This is the command-line tool being used. `sqlmap` is an open-source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over database servers.

- **-r reset.req**: The `-r` flag is used to specify a request file. In this case, `reset.req` is a file that contains the full HTTP request that `sqlmap` will replay to the server to test for SQL injection vulnerabilities. This file typically includes all HTTP headers, parameters, and data, allowing `sqlmap` to properly emulate the request.

- **-p email**: The `-p` flag specifies the parameter that `sqlmap` should focus on. Here, it is set to `email`, meaning that `sqlmap` will specifically target the `email` parameter in the request to check if it is vulnerable to SQL injection.

- **--level 5**: The `--level` flag sets the level of tests to perform. The levels range from 1 to 5, with 5 being the most comprehensive and potentially the most time-consuming. A level of 5 means that `sqlmap` will perform a more thorough and aggressive set of tests.

- **--risk 3**: The `--risk` flag specifies the risk level of the tests. The levels range from 1 to 3, with 3 being the most aggressive. A risk level of 3 indicates that the tests may involve more intrusive and potentially dangerous SQL payloads.

- **--technique=B**: The `--technique` flag specifies the types of SQL injection techniques to use. The options include:
  - `B` for Boolean-based blind
  - `E` for Error-based
  - `U` for Union query-based
  - `T` for Time-based blind
  - `S` for Stacked queries

  In this command, `B` (Boolean-based blind SQL injection) is specified, meaning that `sqlmap` will attempt to exploit vulnerabilities using this particular technique.

### What this command does:
This command runs `sqlmap` to test for SQL injection vulnerabilities on the `email` parameter within the HTTP request specified in the `reset.req` file. It uses a high level of test coverage (`--level 5`), with aggressive SQL payloads (`--risk 3`), and specifically focuses on Boolean-based blind SQL injection techniques (`--technique=B`).

This is typically part of a penetration test where the tester wants to thoroughly check for SQL injection vulnerabilities and potentially exploit them to gain unauthorized access to the database or other sensitive information.


The `-db` option you mentioned appears to be slightly incorrect. If you meant the `-D` option in `sqlmap`, I can explain that, as there is no `-db` option in `sqlmap`.

### `-D` Option in `sqlmap`

The `-D` option in `sqlmap` is used to specify a particular database name that you want to target for further operations. When you use this option, you are telling `sqlmap` to focus on a specific database once it has identified the existence of a SQL injection vulnerability and enumerated the available databases on the server.

### Usage Example:

```bash
sqlmap -u http://example.com/vulnerable.php?id=1 -D database_name --tables
```

### Explanation:
- **-D database_name**: This specifies the database that `sqlmap` should target. Replace `database_name` with the actual name of the database you want to work with.

- **--tables**: This option lists all the tables in the specified database. 

### What this command does:
This command attempts to list all the tables in the database `database_name` located on the server at `http://example.com/vulnerable.php?id=1`. It assumes that a SQL injection vulnerability exists at the `id` parameter of the URL.

### Additional Related Options:
- **-T**: Specifies a table name to target within the selected database.
- **-C**: Specifies a column name to target within the selected table.
- **--dump**: Dumps the contents of the specified database, table, or columns.

### Full Example:

```bash
sqlmap -u http://example.com/vulnerable.php?id=1 -D database_name -T users --dump
```

This command would dump the contents of the `users` table in the `database_name` database.

To download or dump the contents of a database using `sqlmap`, you can use a combination of the `-D` (database), `-T` (table), and `--dump` options. Here’s how you can do it:

### Downloading (Dumping) the Entire Database

If you want to download the entire contents of a specific database, you can do so by specifying the database name with `-D` and then using the `--dump-all` option.

### Example Command:

```bash
sqlmap -u http://example.com/vulnerable.php?id=1 -D database_name --dump-all
```

### Explanation:
- **-u http://example.com/vulnerable.php?id=1**: Specifies the target URL with a vulnerable parameter (`id=1` in this case).
- **-D database_name**: Specifies the database you want to target (replace `database_name` with the actual name of the database).
- **--dump-all**: Dumps all tables and their contents from the specified database.

### Downloading Specific Tables

If you only want to dump specific tables from the database, you can specify the tables using the `-T` option along with the `--dump` flag.

### Example Command:

```bash
sqlmap -u http://example.com/vulnerable.php?id=1 -D database_name -T users --dump
```

### Explanation:
- **-D database_name**: Specifies the database to target.
- **-T users**: Specifies the table to dump (replace `users` with the name of the table you are interested in).
- **--dump**: Dumps the contents of the specified table.

### Downloading Specific Columns

If you only want to dump specific columns from a table, you can further refine the command:

### Example Command:

```bash
sqlmap -u http://example.com/vulnerable.php?id=1 -D database_name -T users -C username,password,email --dump
```

### Explanation:
- **-C username,password,email**: Specifies the columns you want to dump (replace with the actual column names you are interested in).
- **--dump**: Dumps the contents of the specified columns.

### What These Commands Do:
These commands automate the process of extracting data from a vulnerable database through SQL injection. They can retrieve the entire contents of a database, specific tables, or even specific columns, depending on how you configure the command.
