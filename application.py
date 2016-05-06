from flask import Flask, request, render_template
from gensim import corpora, similarities, models
app = Flask(__name__)
app.debug = True

f = open('sample_data.tsv')
books = []
summary = []
for lines in f.readlines():
	lines = lines.split("\t")
	lines[1] = lines[1].replace("\n","")
	books.append(lines[1])  
	summary.append(lines[0])
d = zip(books, summary)
# print d[0][1];

@app.route("/")
def hello():
	return render_template('home.html')

@app.route("/query", methods=['POST'])
def query_get():
	query = str(request.form['search'])
	output = indexing(query)
	return render_template('result.html', data=output)

@app.route("/home")
def home():
	# query = str(request.form['search'])
	# output = indexing(query)
	return render_template('home.html')

@app.route("/100YearsofSolitude")
def YearsofSolitude():
	query = d[0][1]
	output = indexing(query)
	output = output[1:4]			# Top 3 recommendations
	return render_template('100YearsofSolitude.html', data=output)

def indexing(query):
	dictionary = corpora.Dictionary.load('books.dict')
	# corpus = corpora.MmCorpus('books.mm')
	# print books
	# lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
	lsi = models.LsiModel.load('model.lsi')
	index = similarities.MatrixSimilarity.load('sim.index')
	vec_bow = dictionary.doc2bow(query.lower().split())
	vec_lsi = lsi[vec_bow]
	sims = index[vec_lsi]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	name = []
	print len(sims)
	for i in range(len(sims)):
		print i
		print sims[i]
		name.append(books[sims[i][0]])
	print len(name)
	return name

if __name__ == "__main__":
	app.run()