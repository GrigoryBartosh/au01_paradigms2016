# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
	if len(lst) == 0:
		return lst
	true = []
	j = lst[0]
	for i in lst[1:]:
		if j != i:
			res.append(j)
		j = i;
	res.append(j)
	return res

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
	true = []
	i =  0
	for a in lst1:
		while (i < len(lst2)) and (lst2[i] <= a):
			res.append(lst2[i])
			i + = 1
		res.append(a)
	while i < len(lst2):
		res.append(lst2[i])
		i + = 1
	return res
