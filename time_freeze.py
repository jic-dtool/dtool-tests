"""Generate test datasets."""

import os
import time
from collections import namedtuple
import tempfile

import click

from dtoolcore import (
    generate_admin_metadata,
    generate_proto_dataset,
)

TestDataSpec = namedtuple("TestDataSpec", ["size_in_bytes", "num_files"])

test_data_specifications = [
    TestDataSpec(1000, 1000),
    TestDataSpec(1000000, 1),
]


def name_from_dataspec(dataspec):
    return "{}-files-{}-bytes-in-size".format(
        dataspec.num_files,
        dataspec.size_in_bytes
    )


def generate_dataset(prefix, storage, name, size, num_files):
    admin_metadata = generate_admin_metadata(
        name=name,
        creator_username="testing-bot"
    )
    proto_dataset = generate_proto_dataset(
        admin_metadata,
        prefix,
        storage
    )
    proto_dataset.create()

    data_dir = proto_dataset._storage_broker._data_abspath
    for i in range(num_files):
        handle = "{}.txt".format(i)

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(os.urandom(size))
            fp.flush()
            proto_dataset.put_item(fp.name, handle)
            proto_dataset.add_item_metadata(handle, "number", i)

    start = time.time()
    proto_dataset.freeze()
    elapsed = time.time() - start

    print("Freezing {}: {}s".format(name, elapsed))


@click.command()
@click.argument("prefix", default=".")
@click.argument("storage", default="file")
def main(prefix, storage):

    for dataspec in test_data_specifications:
        name = name_from_dataspec(dataspec)
        generate_dataset(
            prefix=prefix,
            storage=storage,
            name=name,
            size=dataspec.size_in_bytes,
            num_files=dataspec.num_files,
        )


if __name__ == "__main__":
    main()
