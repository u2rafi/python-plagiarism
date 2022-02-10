import numpy as np
from io import TextIOWrapper
from typing import Iterable, Any, Union, TextIO, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from plagiarism.sources import Source


class Output(object):
    """
    Class that format ndarray data to a plain format
    :parameter
    data: ndarray
    mapping: mapping of a target array with data (array)
    sorted: is soring data array
    nim_percentage: percentage of minimum marching similarity

    >>> out = Output(data=...)
    >>> out.getlist()
    >>> out.get()
    """

    def __init__(
            self,
            data: np.ndarray,
            *,
            mapping: Optional[list],
            sorted: Optional[bool] = True,
            nim_percentage: Optional[float] = 1.0
    ) -> None:
        self.data = data
        self.map = mapping
        self.sorted = sorted
        self.nim_percentage = nim_percentage

    @staticmethod
    def _sorting(d: Iterable[dict], *, reverse=False) -> Iterable:
        """
        Sorting of an array containing dictionary
        :parameter:
        d: array of dictionary
        reverse: is reverse ordering
        :return:
        a sorted array
        """
        return sorted(d, key=lambda d: d['score'], reverse=reverse)

    def getlist(self) -> List:
        """
        Get list of dictionary in a array
        :return:
        An array
        """
        return list(self._sorting(self._generate_result()) if self.sorted else list(self._generate_result()))

    def get(self) -> List:
        """
        Get an array of values if there are no mapping
        :return:
        An array
        """
        return [dict(score="{:.2f}".format(item[0] * 100)) for item in self.data]

    def _generate_result(self) -> Iterable:
        """ Generator that convert ndarray for an array of dictionary """
        if self.map:
            for index, score in enumerate(self.data):
                _score: float = score[0] * 100
                if _score >= self.nim_percentage:
                    yield dict(doc=self.map[index], score="{:.2f}".format(_score))
        else:
            for item in self.data:
                yield dict(score="{:.2f}".format(item[0] * 100))

    def __call__(self, *args, **kwargs):
        return self.getlist()

    def __iter__(self):
        return self.getlist()


class Plagiarism(object):
    """
    Find plagiarism in a dataset with the given input using scikit-learn (tf-idf algorithm) cosine similarity
    :parameter
    source: `Source` instance having file or file content

    >>> plg = Plagiarism(source=...)
    >>> plg.compare(...).getlist()
    """

    def __init__(
            self,
            source: Source,
            *,
            nim_percentage: Optional[float] = 1.0
    ) -> None:
        self._tfidf_vectorizer = TfidfVectorizer()
        self.source = source
        self.nim_percentage = nim_percentage

    def _cosine_similarity(self, x, y) -> Any:
        """ Compute cosine similarity between samples in x and y. K(x, y) = <Xx, y> / (||x||*||y||) """
        return cosine_similarity(x, y)

    def _get_source(self) -> Union[Iterable, list]:
        return self.source.get_content()

    def _compare_transform(self, raw_document) -> Any:
        tfidf = self._tfidf_vectorizer.fit_transform(list(self._get_source()) + [raw_document])
        return (tfidf * tfidf.T).A[0, 1]

    @staticmethod
    def _get_input_content(f: Union[bytes, TextIO]) -> str:
        if type(f) is bytes:
            return f.decode()
        return f.read()

    def compare(
            self,
            raw_document: Union[TextIOWrapper, TextIO, bytes, str]
    ) -> Output:
        """
        Compare cosine similarity between documents
        :param raw_document: Text file or text contents
        :return:
        Instance of Output
        """

        raw_document = raw_document if type(raw_document) == str else self._get_input_content(raw_document)
        vect_x = self._tfidf_vectorizer.fit_transform(self.source.get_content())
        vect_y = self._tfidf_vectorizer.transform([raw_document])
        similarity = self._cosine_similarity(vect_x, vect_y)
        return Output(data=similarity, mapping=self.source.get_mapping(), nim_percentage=self.nim_percentage)
