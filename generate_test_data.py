"""Generate test datasets."""

import os
import shutil
import time
from collections import namedtuple

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
    return "{}-{}-byte-files".format(
        dataspec.size_in_bytes,
        dataspec.num_files
    )


def generate_dataset(name, size, num_files, output_dir):
    admin_metadata = generate_admin_metadata(
        name=name,
        creator_username="testing-bot"
    )
    proto_dataset = generate_proto_dataset(
        admin_metadata,
        output_dir,
        "file"
    )
    proto_dataset.create()

    data_dir = proto_dataset._storage_broker._data_abspath
    for i in range(num_files):
        fname = "{}.txt".format(i)
        fpath = os.path.join(data_dir, fname)

        with open(fpath, "wb") as fh:
            fh.write(os.urandom(size))

        proto_dataset.add_item_metadata(fname, "number", i)

    start = time.time()
    proto_dataset.freeze()
    elapsed = time.time() - start

    print("Freezing {}: {}s".format(name, elapsed))


def main():

    output_dir = os.path.abspath("datasets")
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    for dataspec in test_data_specifications:
        name = name_from_dataspec(dataspec)
        generate_dataset(
            name=name,
            size=dataspec.size_in_bytes,
            num_files=dataspec.num_files,
            output_dir=output_dir
        )


if __name__ == "__main__":
    main()
