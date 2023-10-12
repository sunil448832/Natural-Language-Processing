# Instagram Page Categorization

## Objective
The objective of this project is to classify Instagram pages into predefined labels, including ["travel," "food," "fashion," "technology," "fitness," and 'others'] based on their content.

## Algorithm
1. **Text Preprocessing:**
   - Download 10 posts uploaded by user and read all .txt files.  
2. **Text Preprocessing:**
   - Tokenization and stopword removal are performed on the content.

3. **Word Embeddings:**
   - Word embeddings are obtained for words present in the embedding vocabulary.
   - If a word is not present in the vocabulary, substrings of words like #fashionshow and #fashionindia are generated, and their word embeddings are obtained.

4. **Dimension Reduction:**
   - Sparse high-dimensional embeddings are transformed into lower dimensions (e.g., dim=5) using UMAP for clustering purposes.

5. **Clustering:**
   - Embeddings are clustered, and cluster centers are identified in the original embedding space.

6. **Label Assignment:**
   - Label embeddings are compared with cluster centroids using cosine similarity.
   - Each cluster is assigned one label with the highest score, resulting in one label for each cluster.
   - The mode of the cluster's label is determined as the final label.

## Installation
To set up the required dependencies, use the following command:

`pip install -r requirements.txt`

## Running the Application
1. Start the backend server using the following command:
`python backend.py`
2. Launch the frontend server with the following command:
`streamlit run frontend.py`
this will open a user interface tab.

## Paste Url in UI
In the user interface, paste profile URLs (e.g., https://www.instagram.com/tunic_branded_kurtis/) into the text field and click the submit button.
