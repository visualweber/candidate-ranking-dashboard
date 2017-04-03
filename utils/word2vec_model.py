from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('./data/duyet_word2vec_skill.bin', binary=True)

def get_relevant_skill(skill):
	try:
		skill = skill.strip().lower()
		skills = model.similar_by_word(skill)
		skills = [ skill[0] for skill in skills ]
		return skills
	except:
		return []