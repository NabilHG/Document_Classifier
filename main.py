import re

def DocClass_Welcome():
    text = """
    Document Classification is typically used in Document Processing for
    assigning categories to documents. Thus, it eases their posterior
    processing and analysis.

    The program “DocumentClassification” classifies an input folder
    containing documents in txt format. It will also receive a file
    containing information about the topics to classify.

    The program will generate the following files:
    A txt file containing the category of the documents
    A txt file containing the statistics of the classification
    """

    print(text)


# function to read all the keywords of every category, given a file
def Read_Categories_Keywords(filename):

    filename = 'ToyExample\keywords_toyExample.txt'
    LCategories = []
    LKeywords = []
    try:
        with open(filename, "r") as f:
            data = f.readlines() # getting the info line by line 
            for line in data: # going through all the data and appending the correct info
                print(line)
                keywords = set(line.split()[1:])
                # splitting, getting the first element, accesing the first element because is a list, then taking the word without :
                category = line.split()[0:1][0][:-1]
                LKeywords.append(keywords)
                LCategories.append(category)
    except ValueError:
        print("Error: provide a file name")
    except FileNotFoundError:
        print("Error: File not found")

    print(f"List of keywords: {LKeywords}")
    print(f"List of categories: {LCategories}")
    return LKeywords, LCategories


def Document_Reader(path, folder_name, filename):
    pass

    # Regular expression to match valid words
    # words = re.findall(r"\b\w+(?:'\w+)?\b", text).lower()


if __name__ == "__main__":
    # DocClass_Welcome()
    Read_Categories_Keywords("test")
