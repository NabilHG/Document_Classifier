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

# function to process statistics of all categories ans keywords
def process_statistics(input_file, output_file):
    category_totals = {}
    document_counts = {}
    keyword_totals = {}
    total_documents = 0

    with open(input_file, 'r') as f:
        content = f.readlines()
        for line in content:
            # unknown categorie or line not containing .txt, skip it
            if "UNKNOWN" in line or ".txt" not in line:
                continue

            total_documents += 1

            # extract category percentages
            percentages = re.findall(r'(\w+):(\d+\.\d+)%', line)
            if percentages:
                for category, percent in percentages:
                    # Initialize category totals and document counts if not already present
                    if category not in category_totals:
                        category_totals[category] = 0.0
                        document_counts[category] = 0
                    # Update the total percentage and document count for the category
                    category_totals[category] += float(percent)
                    document_counts[category] += 1

            # extract keyword counts
            keyword_data = re.findall(r'(\w+):(\d+)', line)
            if keyword_data:
                for keyword, count in keyword_data:
                    # avoid double-counting categories as keywords
                    if f"{keyword}:" not in line:
                        continue
                    # Initialize keywords totals if not already present
                    if keyword not in keyword_totals:
                        keyword_totals[keyword] = 0
                    # Update the total count for the keyword   
                    keyword_totals[keyword] += int(count)

    # calculate the percentage for each category based on total document count
    total_txt_documents = sum(document_counts.values())
    category_percentages = {
        category: (category_totals[category] / total_txt_documents) if total_txt_documents > 0 else 0.0
        for category in category_totals
    }

    # determine the top 10 keywords by total occurrences, sorted
    top_keywords = sorted(keyword_totals.items(), key=lambda x: x[1], reverse=True)[:10]

    # write results to output file
    with open(output_file, 'w') as out_file:
        out_file.write("*** Statistics\n")
        out_file.write(f"Total txt files: {total_documents}\n")
        # write categories sorted 
        for category, percentage in sorted(category_percentages.items(), key=lambda x: x[1], reverse=True):
            out_file.write(f"{category}: {percentage:.2f}%\n")
        
        out_file.write("\n*** Top 10 Keywords\n")
        for keyword, count in top_keywords:
            out_file.write(f"{keyword}: {count}\n")


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
            #skip the output file
            if item == "_DocClassification.txt":
                continue

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
    
    # computing stastistics
    process_statistics("ToyExample\docsToyExample\_DocClassification.txt", "output.txt")
