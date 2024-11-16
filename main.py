import re
import os

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
    #getting the format of the file to check if it is txt
    format_file = filename.split(".")[1] 

    if format_file == "txt":    
        try:
            with open(filename, "r") as f:
                data = f.readlines() # getting the info line by line 
                for line in data: # going through all the data and appending the correct info
                    keywords = set(line.split()[1:]) # getting all minus the first element, because is the category
                    # splitting, getting the first element, accesing the first element because is a list, then taking the word without :
                    category = line.split()[0:1][0][:-1]
                    LKeywords.append(keywords)
                    LCategories.append(category)
        except ValueError:
            print("Error: provide a file name")
        except FileNotFoundError:
            print("Error: File not found")
    else:
        print(f"Attention: the following non txt file has been detected: {filename}")
    
    return LKeywords, LCategories

#function to read all the words of a given file
def Document_Reader(path, folder_name, filename):
    file_path = os.path.join(path, folder_name, filename)

    #getting the format of the file to check if it is txt
    format_file = filename.split(".")[1] 
    if format_file == "txt":    
        try:
            with open(file_path, "r") as f:
                text = f.read()
                # Regular expression to match valid words
                content = re.findall(r"\b\w+(?:'\w+)?\b", text)
                words = [element.lower() for element in content]
        except FileNotFoundError:
            print("Error: File not found")
    else:
        print(f"Attention: the following non txt file has been detected: {filename}")

    return words

# function to count frequencies of keywords per category in text
def Count_Frequencies(LWords, LCategories, LKeywords):
    DFrequencies = {}

    for index, category in enumerate(LCategories):
        DFrequencies[category] = {} # every iteration creating a new category
        for keyword in LKeywords[index]:
            DFrequencies[category][keyword] = LWords.count(keyword) # appending how many times a keyword appear

    return DFrequencies

# function to determine which category belongs the text
def Classify_Doc(DFrequencies):
    total_ocurrencies = 0
    DVotes = {}
    DocCategory = "UNKNOWN"
    
    for category in DFrequencies:
        ocurrencies = 0
        for keyword in DFrequencies[category]:
            ocurrencies += DFrequencies[category][keyword] #value of each keyword
        DVotes[category] = (ocurrencies,)
        total_ocurrencies += ocurrencies

    try:
        for category in DVotes:
            percetange = round((DVotes[category][0] * 100) / total_ocurrencies,2)
            DVotes[category] = DVotes[category] + (percetange,) # concatenating the percetage value, with another tuple because they are immutable
    except ZeroDivisionError:
        print("Error division by zero")

    # finding the maximum in the second element of each tuple, i.e, the percentage
    max_value = max(value[1] for value in DVotes.values()) 
    # finding all the categories with the max_value(percentage)
    max_keys = [category for category, tuple_value in DVotes.items() if tuple_value[1] == max_value]

    if max_value > 50:
        if not len(max_keys) > 1:
            DocCategory = max_keys[0]

    return DVotes, DocCategory


if __name__ == "__main__":
    DocClass_Welcome()
    not_valid = True
    filename= ''
    folder_name = ''
    while not_valid:
        filename = input("Enter the name of the file containing the categories and the keywords:")
        print("The file must be in the same directory of your python script.")
        # checking conditions of validity
        if os.path.exists(filename) and os.path.getsize(filename) != 0:
            not_valid = False

    not_valid = True

    while not_valid:
        folder_name = input("Enter the name of the folder containing the documents:")
        print("The folder must be in the same directory of your python script.")
        # checking conditions of validity
        if os.path.exists(folder_name) and any(item.endswith(".txt") for item in os.listdir(folder_name)):
            not_valid = False
    LKeywords, LCategories = Read_Categories_Keywords(filename)

    output_file = os.path.join(folder_name, "_DocClassification.txt")
    with open(output_file, "w") as output:
        for item in os.listdir(folder_name):
            if item.endswith(".txt"):
                words = Document_Reader(".", folder_name, item)
                DFrequencies = Count_Frequencies(words, LCategories, LKeywords)
                DVotes, DocCategory = Classify_Doc(DFrequencies)

                # write the result in the specified format
                output.write(f"{item}: {DocCategory}(")
                # write category percentages
                percentages = [f"{category}:{round(DVotes[category][1], 2)}%" for category in DVotes]
                output.write(", ".join(percentages) + ")")

                if DocCategory != "UNKNOWN":
                    output.write(": ")
                    # write keyword counts
                    keyword_counts = [f"{keyword}:{DFrequencies[DocCategory].get(keyword, 0)}" for keyword in LKeywords[LCategories.index(DocCategory)]]
                    output.write(", ".join(keyword_counts))

                output.write("\n")
            else:
                output.write(f"Attention: the following non txt file has been detected: {item} in the file {folder_name}_DocClassification.txt")


