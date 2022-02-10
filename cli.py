import sys
from pprint import pprint

import click

from plagiarism.text import Plagiarize


@click.command()
@click.option('-f')
def main(f, **kwargs):
    print(kwargs)
    plg = Plagiarize()
    pprint(plg.find_similarity())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
