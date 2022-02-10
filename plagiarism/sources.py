import os
import pathlib
from typing import Any, Union, List, Iterable, TextIO, Optional, Sized
from bs4 import BeautifulSoup
from urllib import request
import re

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()


class Source(object):

    """
    Base class for dataset as corpus data, source may include file, file stream or web url.
    Subclass must implement `validate()` and `get_content()` so `Plagiarism()` class can call them.
    Extend from `Source` example

    >>> class FileSource(Source):
    >>>     def validate(self):
    >>>         ...
    >>>     def get_content(self):
    >>>         ...
    """

    def __init__(self, source: Any, *, mapping: Optional[List] = None):
        self.source = source
        self.mapping = mapping

    def get_mapping(self) -> Optional[Union[Sized, List, Iterable]]:
        """ A list to map with output """
        return None

    def validate(self) -> bool:
        """ validation of source data """
        raise NotImplementedError

    def get_content(self) -> List[str]:
        """ Get contents from source """
        raise NotImplementedError


class TextSource(Source):

    """ Plain data source """

    def validate(self) -> bool:
        if len(self.source) == 0:
            raise ValueError('Empty string is not allowed.')
        return True

    def get_content(self) -> List[str]:
        return [self.source]


class FileSource(Source):
    """ Input file source """

    @staticmethod
    def _load_file(file: Union[str, TextIO]) -> str:
        """ helper method to load file contents """
        if pathlib.Path(file).exists():
            with pathlib.Path(file).open() as fp:
                return fp.read()
        raise FileNotFoundError('File not found')

    def validate(self) -> bool:
        if pathlib.Path(self.source).exists():
            _, ext = os.path.splitext(self.source)
            with pathlib.Path(self.source).open() as fp:
                if len(fp.read()) > 0:
                    raise ValueError('Empty file not allowed.')
        return True

    def get_content(self) -> List[str]:
        return [self._load_file(self.source)]


class DataSetSource(Source):

    """ This source loads all text file from dataset directory """

    def validate(self) -> bool:
        return True

    def get_mapping(self) -> Optional[Union[Sized, List, Iterable]]:
        """ Load named dataset files from `dataset` in a list """
        docs: list = []
        dataset_dir = os.path.join(BASE_DIR, 'plagiarism/dataset')
        for doc in pathlib.Path(dataset_dir).iterdir():
            docs.append(doc.name)
        return docs

    def get_content(self) -> List[str]:
        """ load file contents of dataset """
        dataset_dir: str = os.path.join(BASE_DIR, 'plagiarism/dataset')
        for ls in pathlib.Path(dataset_dir).iterdir():
            _, ext = os.path.splitext(ls)
            with pathlib.Path(ls).open() as fp:
                yield fp.read()


class WebPageSource(Source):
    """ Web page source to scrap page content """
    def __init__(self, source: Any):
        super(WebPageSource, self).__init__(source)
        self.source = source
        self.pattern = "((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}" \
                       "\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"

    def validate(self) -> bool:
        if re.match(self.pattern, self.source):
            return True
        raise ValueError('Given source is not a valid web url.')

    def get_content(self) -> List[str]:
        self.validate()
        page = request.urlopen(self.source).read()
        soap = BeautifulSoup(page, 'html.parser')
        return [soap.find('body').get_text().strip()]
