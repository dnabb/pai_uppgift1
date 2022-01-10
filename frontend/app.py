# %%
import panel as pn
import param
import requests
from wordcloud import WordCloud
from bokeh.plotting import figure

pn.extension()

SERVER = 'http://127.0.0.1:5000'

def _get_all_texts():
    endpoint = SERVER + '/rest/texts'
    r = requests.get(endpoint)
    texts = r.json()
    return texts

def _get_text(id):
    endpoint = SERVER + '/rest/texts/' + str(id)
    r = requests.get(endpoint)
    text = r.json()['text']
    return text

def _get_freq(id):
    endpoint = SERVER + '/rest/texts/' + str(id) + '/freq'
    r = requests.get(endpoint)
    freq = r.json()['freq']
    return freq

def _make_wordcloud(counter):
    wc = WordCloud().generate_from_frequencies(counter)
    return wc.to_svg()

def _make_plot(freq):
    words = list(freq.keys())
    counts = list(freq.values())
    p = figure(x_range=words, title="Word counts", toolbar_location=None, tools="")
    p.vbar(x=list(freq.keys()), top=counts, width=0.9)
    return p

# _get_text('61d60cd786c4f73416d119f0')
# _get_freq('61d60cd786c4f73416d119f0')

# _get_all_texts

app = pn.template.VanillaTemplate(title='Text Analyser')

all_texts = _get_all_texts()
text_list = [i['_id'] for i in all_texts]
text_selector = pn.widgets.Select(options=text_list, size=len(text_list))
text_viewer = pn.pane.Markdown()
image_viewer = pn.pane.SVG()
chart_viewer = pn.pane.Bokeh()


# %%
def reload_texts():
    all_texts = _get_all_texts()
    text_list = {i['intro']:i['_id'] for i in all_texts}

@pn.depends(text_selector, watch=True, on_init=True) # on_init doesn't work?
def update_main(id):
    text_viewer.object = _get_text(id)
    freq = _get_freq(id)
    image_viewer.object = _make_wordcloud(freq)
    chart_viewer.object = _make_plot(freq)

# %%

app.sidebar.append(text_selector)
main_row = pn.Row(text_viewer, pn.Column(image_viewer, chart_viewer))
app.main.append(main_row)

# %%
app.show()
# %%
