import re

# Define the documents
documents = {
    "Document 1": "The quick brown fox jumped over the lazy dog.",
    "Document 2": "The lazy dog slept in the sun.",
    "Document 3": "The fox is quick and clever."
}

# Create an empty inverted index
inverted_index = {}

# Build the inverted index
for document_id, text in documents.items():

    # Convert text to lowercase
    text = text.lower()

    # Extract words and remove punctuation
    words = re.findall(r'\b\w+\b', text)

    # Add words to inverted index
    for word in words:

        if word not in inverted_index:
            inverted_index[word] = []

        if document_id not in inverted_index[word]:
            inverted_index[word].append(document_id)


# Display the inverted index
print("INVERTED INDEX")
print("-" * 40)

for word in sorted(inverted_index):
    print(word, "->", ", ".join(inverted_index[word]))


# Document retrieval function
def retrieve_documents(query):
    query = query.lower().strip()

    if query in inverted_index:
        return inverted_index[query]
    else:
        return []


# Accept search term
search_term = input("\nEnter a word to search: ")

# Retrieve documents
result = retrieve_documents(search_term)

# Display result
if result:
    print("\nDocuments containing", search_term, ":")
    for document in result:
        print(document)
else:
    print("\nNo documents found for:", search_term)
    print("Aditya Rade   BEAD23167")