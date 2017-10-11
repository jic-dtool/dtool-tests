"""Generate test datasets."""

import os
import shutil

from dtoolcore import (
    generate_admin_metadata,
    generate_proto_dataset,
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

    proto_dataset.freeze()

def main():

    output_dir = os.path.abspath("datasets")
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    generate_dataset(
        name="many_small",
        size=1000,  # Kilobyte
        num_files=1000,
        output_dir=output_dir
    )

    generate_dataset(
        name="one_large",
        size=1000000,  # Megabyte
        num_files=1,
        output_dir=output_dir
    )

if __name__ == "__main__":
    main()
