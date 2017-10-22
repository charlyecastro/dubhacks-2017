import data

def create_tag_freq_table(tags):
	question_map = {}
	for tag in tags:
		question_arr = get_question_for_tag(tag)
		for question in question_arr:
			if question_map[question] is None:
				question_map[question] = 1
			else:
				question_map[question] += 1;

	return question_map

