import sys
import click
from plagiarism.core import Plagiarism
from plagiarism.sources import *
from plagiarism.web.server import app


@click.group()
def main():
    return 0


@click.command()
@click.option('-h', '--host', type=str, default='localhost')
@click.option('-p', '--port', type=str, default=5000)
def runserver(host, port):
    app.run(debug=True, host=host, port=port)


@click.command()
@click.option('-f', '--file', type=click.Path(exists=True), required=False)
@click.option('-t', '--text', type=str, required=False)
@click.option('-w', '--web', type=str, required=False)
@click.option('-d', '--document', type=str, required=False)
def compare(text, file, web, document):
    result = None
    if file:
        result = Plagiarism(DataSetSource('plagiarism/dataset')).compare(open(file).read()).getlist()

    if text:
        result = Plagiarism(TextSource('The Big Bang singularity')).compare(text).getlist()

    if web:
        result = Plagiarism(WebPageSource(web)).compare(document).getlist()

    if result:
        for item in result:
            click.echo(f"{item.get('score')} % similarity in document {item.get('doc', '')} \n")


main.add_command(runserver)
main.add_command(compare)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
