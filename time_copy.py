"""Time the 'dtool copy' command."""

import time

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import click
import dtoolcore


@click.command()
@click.argument("input_uri")
@click.argument("output_prefix")
@click.argument("output_storage", default="file")
def main(input_uri, output_prefix, output_storage):
    StorageBroker = dtoolcore._get_storage_broker(input_uri, None)
    parsed_uri = urlparse(input_uri)

    for uri in StorageBroker.list_dataset_uris(parsed_uri.path, None):
        dataset = dtoolcore.DataSet.from_uri(uri)
        name = dataset.name

        start = time.time()
        dtoolcore.copy(uri, output_prefix, output_storage)
        elapsed = time.time() - start
        print("Copying {} took: {}s".format(name, elapsed))


if __name__ == "__main__":
    main()
