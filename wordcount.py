"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys

def read_words(filename):
	words = []
	dict = {}
	with open(filename, "r") as f:
		for line in f:
			for s in line.split():
				t = s.lower()
				dict[t] = dict.get(t,0) + 1
	for w in dict:
		words.append((w,dict[w]))
	return words

def print_words(filename):
	words = read_words(filename)
	words.sort(key=lambda x: x[0])
	for w in words:
		print(w[0], w[1])

def print_top(filename):
	words = read_words(filename)
	words.sort(key=lambda x: -x[1])
	l = len(words) if len(words) <= 20 else 20
	for i in range(l):
		print(words[i][0], words[i][1])

# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
	if len(sys.argv) != 3:
		print('usage: ./wordcount.py {--count | --topcount} file')
		sys.exit(1)

	option = sys.argv[1]
	filename = sys.argv[2]
	if option == '--count':
		print_words(filename)
	elif option == '--topcount':
		print_top(filename)
	else:
		print('unknown option: ' + option)
		sys.exit(1)

if __name__ == '__main__':
	main()
