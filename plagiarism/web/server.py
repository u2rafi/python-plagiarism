import json
from flask import Flask, views, render_template, request
from plagiarism.core import Plagiarism
from plagiarism.sources import (
    TextSource,
    WebPageSource,
    DataSetSource
)

app = Flask(__name__)
app.secret_key = 'uRRGWtmxUgZuj69KTcf5ey8RCWyDjAcC3EVBH7XtYzxTwxvezA9qKS6cEvGzFvNy'


class IndexView(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            kind = request.form.get('kind')
            match_range = request.form.get('range', 1)
            result = list()

            if kind == 'single_file':
                file = request.files['file']
                dp = DataSetSource('plagiarism/dataset')
                result = Plagiarism(dp, nim_percentage=int(match_range)).compare(file.stream.read().decode()).getlist()

            if kind == 'text_input':
                dp = DataSetSource('plagiarism/dataset')
                plz = Plagiarism(dp, nim_percentage=int(match_range))
                result = plz.compare(request.form.get('text')).getlist()

            if kind == 'compare_documents':
                doc1 = request.files.get('doc1')
                doc2 = request.files.get('doc2')
                result = Plagiarism(TextSource(doc1.stream.read().decode())).compare(doc2.stream.read()).get()

            if kind == 'webpage':
                link = request.form.get('link')
                text = request.form.get('text')
                result = Plagiarism(source=WebPageSource(link)).compare(text).get()

            return json.dumps({'success': True, 'result': result})
        return render_template('index.html')


app.add_url_rule('/', view_func=IndexView.as_view('index'))

if __name__ == '__main__':
    app.run(debug=True)
