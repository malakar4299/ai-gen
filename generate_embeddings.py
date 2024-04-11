import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import os

# Load the pre-trained sentence transformer model
# model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to load data from the JSON file
def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # print(file.readline()) 
    return data

# Function to generate embeddings for a list of texts
def generate_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings

def find_similar_repositories(embeddings, repo_details, threshold=0.7):
    # Calculate cosine similarity matrix
    sim_matrix = cosine_similarity(embeddings)
    
    similar_repos = []
    
    # Iterate over the matrix to find embeddings with high similarity
    for i in range(len(sim_matrix)):
        for j in range(i + 1, len(sim_matrix)):
            if sim_matrix[i][j] > threshold:
                similar_repos.append((repo_details[i]['repo_info']['full_name'], repo_details[j]['repo_info']['full_name'], sim_matrix[i][j]))
    
    # Sort the pairs by similarity for easier reading
    similar_repos.sort(key=lambda x: x[2], reverse=True)
    
    return similar_repos

# Store embeddings to file
def save_embeddings(embeddings, filename='embeddings_new.npy'):
    np.save(filename, embeddings)

# Load embeddings from file
def load_embeddings(filename='embeddings_new.npy'):
    return np.load(filename)

def load_model_if_exists(model_path, documents):
    if os.path.exists(model_path):
        print(f"Loading model from {model_path}")
        model = Doc2Vec.load(model_path)
        return model
    else:
        print(f"Model file not found at {model_path}.")
        model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4, epochs=40)
        model.save("repo_doc2vec.model")  
        return model

def DocToVecGenerateEmbeddings(model, repo_details):
    # To infer a vector for an existing document in the training corpus
    vector = model.dv[str(repo_details[0]['repo_info']['id'])]  # Using the tag

    # To infer a vector for a new document
    new_doc_vector = model.infer_vector(["new", "document", "words"])
    # Assuming repo_details is a list of repositories, each with its readme text
    # If it's a single repository, wrap it in a list: [repo_details]

    similar_docs = model.dv.most_similar(str(repo_details[0]['repo_info']['id']), topn=5)

    return similar_docs
# Main function to process the JSON file and generate embeddings
def main(json_file):
    repo_details = load_data(json_file)

    # Doc to Vec Model

    documents = [TaggedDocument(words=detail['readme'].split(), tags=[str(detail['repo_info']['id'])]) for detail in repo_details if 'readme' in detail and detail['readme']]

    model = load_model_if_exists("repo_doc2vec.model", documents)

    similar_docs = DocToVecGenerateEmbeddings(model, repo_details)

    print(similar_docs) 

    # Sentence Tokenizer model - uncomment all below
    
    # texts = [repo['readme'] for repo in repo_details if 'readme' in repo and repo['readme']]
    
    # # Generate embeddings for each piece of text
    # embeddings = generate_embeddings(texts)

    # # Save embeddings to file
    # save_embeddings(embeddings)
    # print("Embeddings saved to file.")
    
    # # Optionally, you can do something with the embeddings here, like saving them, or calculating similarities
    # similar_repos = find_similar_repositories(embeddings, repo_details)
    # for pair in similar_repos:
    #     print(f"Similar Repositories: {pair[0]} and {pair[1]} with similarity {pair[2]:.2f}")

if __name__ == "__main__":
    json_file_path = './repo_details_new.json'  # Update this path to your actual JSON file location
    main(json_file_path)
