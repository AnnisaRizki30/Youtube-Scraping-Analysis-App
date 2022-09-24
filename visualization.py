import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns

plt.rcParams['figure.figsize'] = 12, 8


# Function to make a wordcloud
def render_word_cloud(corpus):
    '''Generates a word cloud using all the words in the corpus.
    '''
    fig_file = BytesIO()
    wordcloud = WordCloud(width=1600, height=800,max_font_size=200, background_color='black', colormap = 'Dark2', stopwords=STOPWORDS).generate(corpus)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)
    fig_data_png = fig_file.getvalue()
    result = base64.b64encode(fig_data_png)
    return result.decode('utf-8')


# Function to make a bar graph
def bar_graph(dataframe=None):
    '''Generates bar graph using comments dataframe.
    '''
    fig_file = BytesIO()
    x = dataframe.sentiment
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.set_palette('Set2')
    class_names = ['positive', 'negative', 'neutral']
    bar = sns.countplot(x=x)
    bar.set(xticklabels=[])  
    bar.set_xticklabels(class_names)
    bar.set(xlabel=None)
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)
    fig_data_png = fig_file.getvalue()
    result = base64.b64encode(fig_data_png)
    return result.decode('utf-8')


# Function to make a donut chart that will use in pie graph
def donut(sizes, ax, angle=90, labels=None,colors=None, explode=None, shadow=None):
    ax.pie(sizes, colors = colors, labels=labels, autopct='%.1f%%', 
           startangle = angle, pctdistance=0.8, explode = explode, 
           wedgeprops=dict(width=0.4), shadow=shadow)
    plt.axis('equal')  
    plt.tight_layout()


# Function to make a pie graph
def pie_graph(dataframe=None):
    '''Generates pie graph using comments dataframe.
    '''
    fig_file = BytesIO()
    df = dataframe
    sizes = dataframe.sentiment.value_counts()
    labels = ['Positive', 'Negative', 'Neutral']
    colors = ['lightskyblue', 'lightcoral', 'lightgreen']
    explode = (0,0,0)

    fig, ax = plt.subplots(figsize=(6,4))
    donut(sizes, ax, 90, labels, colors=colors, explode=explode, shadow=True)
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)
    fig_data_png = fig_file.getvalue()
    result = base64.b64encode(fig_data_png)
    return result.decode('utf-8')