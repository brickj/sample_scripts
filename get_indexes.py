import requests

# list_of_nodes = ["localhost:9102", "localhost:9100", "localhost:9103"]
list_of_nodes = ["localhost:9102"]

dict_name_create_statement = {}
list_of_buckets = []
bucket = str()

for node in list_of_nodes:

    response = requests.get(
        "http://" + node + "/getIndexStatement", auth=("<ADMIN>", "<PASSWORD>")
    )

    path = "<PATH_TO_FILE>/indexes.txt"
    text_file = open(path, "w")

    for i in range(len(response.json())):
        line = response.json()[i]

        index_INDEX_start = "INDEX"
        index_ON_end = "ON"

        index_name = line[
            line.find(index_INDEX_start)
            + len(index_INDEX_start) : line.find(index_ON_end)
        ].replace("`", "")

        if 'WITH {  "defer_build":true }' in line:
            index_INDEX_start = "ON"
            index_ON_end = "("
            bucket = line[
                line.find(index_INDEX_start)
                + len(index_INDEX_start) : line.find(index_ON_end)
            ].replace("`", "")

        if not bucket in list_of_buckets:
            list_of_buckets.append(bucket)

        if not index_name in dict_name_create_statement:
            line = line.replace("\\", "")
            line = line.replace("_", "-")
            line = line.replace("defer-build", "defer_build")

            if 'WITH {  "defer_build":true }' in line:
                line = line.replace('WITH {  "defer_build":true }', "")

            dict_name_create_statement[index_name] = line

    for value in dict_name_create_statement.values():
        text_file.write(value + ";\n")

text_file.close()
