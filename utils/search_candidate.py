from scipy import spatial
import pandas as pd
import numpy as np
import re

from word2vec_model import *

candidate_index_path = './data/candidate_skills_vector_test.csv'

def avg_feature_vector(words, model, num_features):
        #function to average all words vectors in a given paragraph
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        #list containing names of words in the vocabulary
        index2word_set = set(model.index2word) # this is moved as input param for performance reasons
        for word in words:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if(nwords>0):
            featureVec = np.divide(featureVec, nwords)
        return featureVec
    
def find_best_candidate_by_skills(skills, number_of_result = 10):
    top_results = []
    input_skill_vector = avg_feature_vector(skills.split(), model=model, num_features=300)
    
    def update_result(top_results, candidate_id, score, number_of_result):
        top_results.append({ 'candidate_id': candidate_id, 'score': score })
        top_result_sorted = sorted(top_results, key=lambda k: k['score'], reverse=True) 
        top_results = top_result_sorted[:number_of_result]
        return top_results

    chunksize = 10 ** 5
    for candidates in pd.read_csv(candidate_index_path, chunksize=chunksize, error_bad_lines=False):
        for i, candidate in candidates.iterrows():
            candidate_feature = candidate[2]
            candidate_feature = re.sub(' +', ' ', candidate_feature)
            candidate_feature = candidate_feature.replace('\n', '').replace('[', '').replace(']', '').strip().split(' ')
            candidate_feature = np.array(candidate_feature, dtype="float32")
            
            similarity =  1 - spatial.distance.cosine(input_skill_vector, candidate_feature)
            top_results = update_result(top_results, candidate_id=candidate[0], score=similarity, number_of_result=number_of_result)
    return top_results

def find_candidate_by_skill(skills, limit = 10):
	"""Find candidate from index, input is array of skills"""
	skills = ' '.join(skills)

	return find_best_candidate_by_skills(skills, number_of_result=limit)