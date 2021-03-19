# sample_scripts

- The purpose of this repository is to share small, practical, automation scripts.
- Modify get_indexes.py file to include cluster nodes in the list_of_nodes.
Modify get_indexes.py path variable for the desired output path for the indexes.txt file.
Run get_indexes.py and execute the followind command using cbq eg:
cbq -networkconfig external -e couchbases://cb9b5e01-2c99-48d1-8191-1727e1929bd5.dp.cloud.couchbase.com -u <DB_USER_NAME> -p <PASSWORD> -no-ssl-verify -f indexes.txt

