import pathlib
import os
import pytest
from plagiarism.sources import (
    TextSource,
    FileSource,
    DataSetSource,
    WebPageSource
)

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()


@pytest.fixture
def text_source():
    return TextSource("the Big Bang singularity")


@pytest.fixture
def webpage_source():
    return WebPageSource('https://en.wikipedia.org/wiki/Big_Bang')


@pytest.fixture
def dataset_source():
    return DataSetSource('plagiarism/dataset')


@pytest.fixture
def file_source():
    doc1 = os.path.join(BASE_DIR, 'dataset/africa_history.txt')
    return FileSource(doc1)


class TestClass:
    def test_webpage_content(self, webpage_source):
        assert webpage_source.get_content() != None

    def test_dataset_source(self):
        s = DataSetSource('plagiarism/dataset')
        assert s.validate() == True
        assert s.get_content() != None
        assert s.get_mapping() != None

    def test_get_content(self):
        s = DataSetSource('plagiarism/dataset')
        assert s.get_content() != None

    def test_text_source(self, text_source):
        assert text_source.validate() == True
        # assert text_source._load_file('test_input.txt') != None
        assert text_source.get_content() != None

    def test_file_source(self, file_source):
        assert file_source.validate() == True

    def test_wepage_source(self, webpage_source):
        assert webpage_source.validate() == True

    def test_wepage_source_content(self, webpage_source):
        assert webpage_source.get_content() != None
