import pathlib
import os
import pytest
import unittest
from plagiarism.sources import (
    TextSource,
    FileSource,
    DataSetSource,
    WebPageSource, Source
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
        assert text_source.get_content() != None

    def test_wepage_source(self, webpage_source):
        assert webpage_source.validate() == True

    def test_wepage_source_content(self, webpage_source):
        assert webpage_source.get_content() != None


class ExceptionTestCase(unittest.TestCase):

    def test_source_validate_method(self):
        s = Source('test')
        self.assertRaises(NotImplementedError, s.validate)

    def test_web_validate_method(self):
        s = WebPageSource('Big_Bang')
        self.assertRaises(ValueError, s.validate)

    def test_source_get_content(self):
        s = Source('test')
        self.assertRaises(NotImplementedError, s.get_content)

    def test_source_get_mapping(self):
        s = Source('test')
        self.assertEqual(s.get_mapping(), None)

    def test_dataset_content_not_none(self):
        s = DataSetSource('plagiarism/dataset')
        self.assertIsNotNone(list(s.get_content()))

    def test_text_validate_value_error(self):
        s = TextSource('')
        self.assertRaises(ValueError, s.validate)

    def test_file_content_not_none(self):
        doc1 = os.path.join(BASE_DIR, 'plagiarism/dataset/africa_history.txt')
        s = FileSource(doc1)
        self.assertIsNotNone(s.get_content())

    def test_file_validate_not_found(self):
        doc1 = os.path.join(BASE_DIR, 'africa_history.txt')
        s = FileSource(doc1)
        self.assertRaises(FileNotFoundError, s.validate)

    def test_file_validate_value_error(self):
        doc1 = os.path.join(BASE_DIR, 'tests/empty.txt')
        s = FileSource(doc1)
        self.assertRaises(ValueError, s.validate)

    def test_file_get_content_not_found(self):
        s = FileSource('dataset/africa_history.txt')
        self.assertIsNotNone(FileNotFoundError, s.get_content)
