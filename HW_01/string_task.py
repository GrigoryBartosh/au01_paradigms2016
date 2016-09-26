# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'
def verbing(s):
	if len(s) < 3:
		return s
	if s[-3:] == 'ing':
		return s+'ly'
	return s+'ing'

# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'
def not_bad(s):
	a = s.find('not')
	b = s.find('bad')
	if (a == -1) or (b == -1) or (a > b):
		return s
	return s[0:a] + 'good' + s[b+3:]
