# From: http://dataexperiments.net/2015/01/31/using-lexrank-to-summarize-textusing-sumy-py/
# Import library essentials
from sumy.parsers.plaintext import PlaintextParser  # We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer  # We're choosing Lexrank, other algorithms are also built in
from sumy.summarizers.text_rank import TextRankSummarizer

file = "JustText.txt"  # name of the plain-text file
parser = PlaintextParser.from_file(file, Tokenizer("english"))

print "Lex Rank:"
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, 3)  # Summarize the document with N sentences

for sentence in summary:
    print sentence

print "Text Rank:"
summarizer = TextRankSummarizer()

summary = summarizer(parser.document, 3)  # Summarize the document with N sentences

for sentence in summary:
    print sentence
