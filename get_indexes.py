import requests

# list_of_nodes = ["localhost:9102", "localhost:9100", "localhost:9103"]
list_of_nodes = ["localhost:9102"]

dict_name_create_statement = {}
list_of_buckets = []


def check_create_primary():
    global index_INDEX_start, index_ON_end, bucket
    if not "CREATE PRIMARY INDEX" in line:
        index_INDEX_start = "ON"
        index_ON_end = "("
        bucket = line[
            line.find(index_INDEX_start)
            + len(index_INDEX_start) : line.find(index_ON_end)
        ].replace("`", "")


def check_primary():
    global index_INDEX_start, index_ON_end, bucket
    if "INDEX `#primary`" in line:
        index_INDEX_start = "ON"
        index_ON_end = "("
        bucket = line[
            line.find(index_INDEX_start) + len(index_INDEX_start) : len(line)
        ].replace("`", "")


for node in list_of_nodes:

    response = requests.get(
        "http://" + node + "/getIndexStatement", auth=("admin", "password")
    )

    path = "/Users/rickjacobs/Downloads/indexes.txt"
    text_file = open(path, "w")

    print(response.json())

    for i in range(len(response.json())):
        line = response.json()[i]

        print(line)

        index_INDEX_start = "INDEX"
        index_ON_end = "ON"

        index_name = line[
            line.find(index_INDEX_start)
            + len(index_INDEX_start) : line.find(index_ON_end)
        ].replace("`", "")

        check_create_primary()

        check_primary()

        if not bucket in list_of_buckets:
            list_of_buckets.append(bucket)

        if not index_name in dict_name_create_statement:
            line = line.replace("\\", "")
            line = line.replace("_", "-")
            line = line.replace("defer-build", "defer_build")

            dict_name_create_statement[index_name] = line

    for bucket in list_of_buckets:
        bucket = bucket.strip()

        print(bucket)
        dict_name_create_statement[bucket] = (
            "BUILD INDEX ON `"
            + bucket
            + "` ((SELECT RAW name FROM system:indexes WHERE keyspace_id = '"
            + bucket
            + "' AND state = 'deferred'))"
        )

    for value in dict_name_create_statement.values():
        text_file.write(value + ";\n")

text_file.close()
