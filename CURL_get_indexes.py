import requests

response = requests.get('http://localhost:9102/getIndexStatement', auth=('admin', 'password'))
path = '/Users/rickjacobs/Downloads/indexes_FINAL.txt'
text_file = open(path, "w")

for i in range(len(response.json())):

    line = response.json()[i]
    line = line.replace("\\", "")
    line = line.replace("_", "-")
    line = line.replace("defer-build", "defer_build")
    line = line + '\n'

    text_file.write(line)

text_file.close()

