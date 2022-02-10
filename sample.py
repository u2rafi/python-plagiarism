import os
import pathlib

from plagiarism.core import Plagiarism
from plagiarism.sources import *

if __name__ == '__main__':
    here = pathlib.Path(__file__).parent.resolve()
    doc1 = os.path.join(here, 'plagiarism/dataset/africa_history.txt')
    doc2 = os.path.join(here, 'plagiarism/dataset/africa_history_copy.txt')
    doc3 = os.path.join(here, 'plagiarism/dataset/mesopotamia.txt')
    doc4 = os.path.join(here, 'plagiarism/dataset/big_bang.txt')
    doc5 = os.path.join(here, 'plagiarism/dataset/egyptology.txt')
    dsp = DataSetSource(source='plagiarism/plagiarism/dataset')
    ifp = FileSource(source=doc1)
    wpp = WebPageSource(source='https://en.wikipedia.org/wiki/History_of_religion')
    tp = TextSource(source='ancient Egyptians')
    # print(Plagiarism(content=DataSetProvider('plagiarism/dataset')).compare('ancient Egyptians').getlist())
    # print(Plagiarism(content=DataSetProvider('plagiarism/dataset')).compare(doc2))
    print(Plagiarism(DataSetSource('plagiarism/dataset')).compare(open(doc2).read()).getlist())
    # print(Plagiarism(content=InputFileProvider(doc5)).compare('ancient Egyptians'))
    print(Plagiarism(source=FileSource(doc1)).compare(open(doc2).read()).get())
    # print(Plagiarism(content=WebPageProvider(source='https://en.wikipedia.org/wiki/History_of_religion')).compare(
    #     'History of religion'))
    print(Plagiarism(WebPageSource(source='https://en.wikipedia.org/wiki/Big_Bang')).compare(doc4))
