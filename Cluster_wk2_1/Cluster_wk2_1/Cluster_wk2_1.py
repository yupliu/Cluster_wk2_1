import graphlab
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn
except ImportError:
    pass

from distutils.version import StrictVersion
assert (StrictVersion(graphlab.version) >= StrictVersion('1.8.5')),'GraphLab Create must be version 1.8.5 or later.'
wiki = graphlab.SFrame('C:\\Machine_Learning\\Cluster_wk2_1\\people_wiki.gl\\')
wiki
wiki['word_count']=graphlab.text_analytics.count_words(wiki['text'])
model = graphlab.nearest_neighbors.create(wiki,label='name',features = ['word_count'],method='brute_force',distance='euclidean')
bo = model.query(wiki[wiki['name']=='Barack Obama'],label='name',k=10)
def top_words(name):
    """
    Get a table of the most frequent words in the given person's wikipedia page.
    """
    row = wiki[wiki['name'] == name]
    word_count_table = row[['word_count']].stack('word_count', new_column_name=['word','count'])
    return word_count_table.sort('count', ascending=False)
obama_words = top_words('Barack Obama')
obama_words
barrio_words = top_words('Francisco Barrio')
barrio_words
combined_words = obama_words.join(barrio_words,on='word')
combined_words = combined_words.rename({'count':'Obama','count.1':'Barrio'})
combined_words.sort('Obama', ascending=False)
common_words = set(combined_words['word'][0:5])

def has_top_words(word_count_vector):
    # extract the keys of word_count_vector and convert it to a set
    unique_words = set(word_count_vector.keys())   # YOUR CODE HERE
    print 'length of unique words = ' + str(len(unique_words))
    # return True if common_words is a subset of unique_words
    # return False otherwise
    return common_words.issubset(unique_words)  # YOUR CODE HERE

wiki['has_top_words'] = wiki['word_count'].apply(has_top_words)

# use has_top_words column to answer the quiz question
wiki_has_top_words = wiki[wiki['has_top_words']==1L] # YOUR CODE HERE
type(wiki_has_top_words)
print wiki_has_top_words.num_rows()

print 'Output from your function:', has_top_words(wiki[32]['word_count'])
print 'Correct output: True'
print 'Also check the length of unique_words. It should be 167'

print 'Output from your function:', has_top_words(wiki[33]['word_count'])
print 'Correct output: False'
print 'Also check the length of unique_words. It should be 188'

bo = wiki[wiki['name']=='Barack Obama']['word_count'][0]
gb = wiki[wiki['name']=='George W. Bush']['word_count'][0]
jb = wiki[wiki['name']=='Joe Biden']['word_count'][0]

bg = graphlab.toolkits.distances.euclidean(bo,gb)
bj = graphlab.toolkits.distances.euclidean(bo,jb)
gj = graphlab.toolkits.distances.euclidean(gb,jb)

def unique_words(name):
    word_count_vector = wiki[wiki['name']== name]['word_count'][0]
    unique_words = set(word_count_vector.keys())
    return unique_words

obama_unique_words = unique_words('Barack Obama')
bush_unique_words = unique_words('George W. Bush')
common_obama_bush = obama_unique_words.intersection(bush_unique_words)

