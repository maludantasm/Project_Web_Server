def config(archive):
    docs = archive.readline().split('-')[1][:-1]
    errors = archive.readline().split('-')[1]
    return docs, errors
