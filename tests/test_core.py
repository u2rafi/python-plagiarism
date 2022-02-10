import os
import pathlib
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from plagiarism.core import Plagiarism, Output
from plagiarism.sources import (
    TextSource,
    WebPageSource,
    FileSource,
    DataSetSource,
)

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()


class TestClass:
    def test_core_plagiarism(self):
        doc1 = os.path.join(BASE_DIR, 'plagiarism/dataset/africa_history.txt')
        plg = Plagiarism(DataSetSource('plagiarism/dataset'))
        plg.compare('the Big Bang singularity').getlist()
        plg.compare('the Big Bang singularity').get()
        plg._get_source()
        plg._compare_transform('Big Bang')
        # plg._cosine_similarity()
        assert plg._get_input_content(open(doc1)) != None

    def test_output(self):
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(['the Big Bang singularity', 'Big Bang'])
        similarity = (tfidf * tfidf.T).A

        vect_x = vectorizer.fit_transform(['the Big Bang singularity'])
        vect_y = vectorizer.transform(['Big Bang'])

        out = Output(data=similarity, mapping=None, nim_percentage=0)
        out.__iter__()
        out.__call__()
        out._generate_result()
        assert (tfidf * tfidf.T).A[0, 1] > 0
        assert out._sorting(out._generate_result()) != None
        assert out.getlist() != None
        assert out.get() != None

    def test_similarity_file_source(self):
        doc1 = os.path.join(BASE_DIR, 'plagiarism/dataset/africa_history.txt')
        result = Plagiarism(source=FileSource(doc1)).compare(open('test_input.txt').read()).getlist()
        assert len(result) > 0

    def test_similarity_text_source(self):
        src = TextSource("the Big Bang singularity")
        plg = Plagiarism(src).compare('the Big Bang singularity')
        assert len(plg.getlist()) > 0

    def test_similarity_webpage_source(self):
        src = WebPageSource(source='https://en.wikipedia.org/wiki/Big_Bang')
        plg = Plagiarism(src).compare('the Big Bang singularity')
        assert len(plg.getlist()) > 0