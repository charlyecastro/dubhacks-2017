from data import get_question_for_tag

def create_tag_freq_table(tags):
	question_map = {}
	for tag in tags:
		question_arr = get_question_for_tag(tag)
		for question in question_arr:
			if question not in question_map:
				question_map[question] = 1
			else:
				question_map[question] += 1;

	return question_map

def test():
	tags = ['orientation', 'advice']
	qmp = create_tag_freq_table(tags)
	print(qmp)
