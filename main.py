import hashlib
import os
import time
import zlib


def write_obj(objtype, content):
    data = f"{objtype} {len(content)}\0".encode() + content
    sha1 = hashlib.sha1(data)
    hex_sha1 = sha1.hexdigest()
    path = f".git/objects/{hex_sha1[:2]}/{hex_sha1[2:]}"
    os.makedirs(path, exist_ok=True)
    with open(path, "wb") as f:
        f.write(zlib.compress(data))
    return sha1


def write_blob(content):
    return write_obj("blob", content.encode())


def write_tree(filenames, hashes):
    mode = 100644
    entries = b""
    for name, _hash in zip(filenames, hashes):
        entries += f"{mode} {name}\0".encode() + _hash
    return write_obj("tree", entries)


def write_commit(tree_sha1, parents, author, committer, message):
    content = f"tree {tree_sha1}\n"
    for parent in parents:
        content += f"parent {parent}\n"
    content += f"author {author} {int(time.time())} {time.strftime('%z')}\n"
    content += f"committer {committer} {int(time.time())} {time.strftime('%z')}\n"
    content += "\n"
    content += message
    return write_obj("commit", content.encode())


def write_branch(name, _hash):
    with open(f".git/refs/heads/{name}", "w") as f:
        f.write(_hash)
