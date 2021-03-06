"""Generate test datasets."""

import os
import time
from collections import namedtuple
import tempfile
import cProfile

import click

from dtoolcore import (
    generate_admin_metadata,
    generate_proto_dataset,
)

TestDataSpec = namedtuple("TestDataSpec", ["size_in_bytes", "num_files"])

test_data_specifications = [
    TestDataSpec(10, 1),
    TestDataSpec(10, 5),
    TestDataSpec(10, 10),
#    TestDataSpec(10, 25),
#    TestDataSpec(10, 50),
#    TestDataSpec(10, 100),
#    TestDataSpec(10, 500),
#    TestDataSpec(10, 1000),
#   TestDataSpec(1000, 1000),
#   TestDataSpec(1000000, 1),
]


def name_from_dataspec(dataspec):
    return "{}-files-{}-bytes-in-size".format(
        dataspec.num_files,
        dataspec.size_in_bytes
    )


def generate_dataset(base_uri, name, size, num_files):
#   print(
#       "Generating dataset in {} with {} files of size {} bytes".format(
#           storage, num_files, size
#       )
#   )
    admin_metadata = generate_admin_metadata(
        name=name,
        creator_username="testing-bot"
    )
    proto_dataset = generate_proto_dataset(
        admin_metadata,
        base_uri
    )
    proto_dataset.create()
    proto_dataset.put_readme("")

    for i in range(num_files):
        handle = "{}.txt".format(i)

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(os.urandom(size))
            fp.flush()
            proto_dataset.put_item(fp.name, handle)
            proto_dataset.add_item_metadata(handle, "number", i)

    start = time.time()
#   cProfile.runctx("proto_dataset.freeze()", {"proto_dataset": proto_dataset}, {}, sort="cumtime")
    proto_dataset.freeze()
    elapsed = time.time() - start

#   print("Freezing {} took: {}s".format(name, elapsed))
    print("{},{}".format(num_files, elapsed))


@click.command()
@click.argument("base_uri", default=".")
def main(base_uri):

    for dataspec in test_data_specifications:
        name = name_from_dataspec(dataspec)
        generate_dataset(
            base_uri=base_uri,
            name=name,
            size=dataspec.size_in_bytes,
            num_files=dataspec.num_files,
        )


if __name__ == "__main__":
    main()
