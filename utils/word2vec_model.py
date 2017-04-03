from gensim.models import KeyedVectors
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
model = KeyedVectors.load_word2vec_format(dir_path + '/../data/duyet_word2vec_skill.bin', binary=True)

def get_relevant_skill(skill):
	try:
		skill = skill.strip().lower()
		skills = model.similar_by_word(skill)
		skills = [ skill[0] for skill in skills ]
		return skills
	except:
		return []
