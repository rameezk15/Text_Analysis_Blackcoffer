import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import syllables

# Download the 'punkt', 'stopwords', 'words' resource
nltk.download(['punkt', 'stopwords', 'words'])

def load_stopwords_from_folder(stopwords_folder_path):
    stopwords_file_list = os.listdir(stopwords_folder_path)
    stop_words = []
    for file in stopwords_file_list:
        file_path = os.path.join(stopwords_folder_path, file)
        with open(file_path, 'r', encoding='latin-1') as inf:
            stop_words.extend(word_tokenize(inf.read()))
    return stop_words

def clean_text(text, load_stop_words, stop_words):
    text_words_list = word_tokenize(text)
    filter_words = [word.lower() for word in text_words_list
                    if word.lower() not in load_stop_words
                    and word.lower() not in string.punctuation
                    and word.lower() not in stop_words]
    return filter_words

def filter_text_data(article_folder_path, load_stop_words, stop_words):
    filter_data = {}
    text_data = {}
    article_files = os.listdir(article_folder_path)
    for file in article_files:
        file_path = os.path.join(article_folder_path, file)
        with open(file_path) as inf:
            text = inf.read()
        # Create text_data dict and filter_data dict
        file_name = file.split('.')[0]
        text_data[file_name] = text
        filter_words = clean_text(text, load_stop_words, stop_words)
        filter_data[file_name] = filter_words
    return filter_data, text_data

def filter_master_dictionary(MasterDictionary_folder_path, load_stop_words):
    MasterDictionary = {}
    file_list = os.listdir(MasterDictionary_folder_path)
    for file in file_list:
        file_path = os.path.join(MasterDictionary_folder_path, file)
        with open(file_path, 'r', encoding='latin-1') as inf:
            file_name = file.split(".")[0]
            words = word_tokenize(inf.read())
            MasterDictionary[file_name] = [word.lower() for word in words if word.lower() not in load_stop_words]
    return MasterDictionary

def complex_word_count(words):
    complex_word_list = [word for word in words if syllables.estimate(word)>2]
    count = len(complex_word_list)
    return count

def syllable_count_per_word(words):
    exceptions = ("es","ed")
    syllable_count_list = [syllables.estimate(word[:-2]) if word.endswith(exceptions) else syllables.estimate(word) for word in words]
    total_syllable_count = sum(syllable_count_list)
    return total_syllable_count

def avg_sentence_length(text):
    sentences_count = len(text.split('.'))
    word_count = len(text.split(" "))
    avg_length = word_count/sentences_count
    return avg_length

def personal_pronouns(text):
    pronoun_pattern = re.compile(r'\b(?:I|we|my|ours|us)\b', re.IGNORECASE)
    matches = pronoun_pattern.findall(text)
    matches = [match for match in matches if match != "US"]
    return len(matches)

def create_output_df(output_dict):
        output_df = import_output_data_structure()
        for url_id, data_dict in output_dict.items():
                output_df.loc[output_df['URL_ID']==url_id, data_dict.keys()] = data_dict.values()
        return output_df

def import_output_data_structure():
    file_path = os.path.join(os.getcwd(), 'Input', 'Output Data Structure.xlsx')
    return pd.read_excel(file_path)

def export_to_excel(output_df):
     output_df.to_excel('output_file.xlsx', index=False)

def output_dict(text_data, filter_data, MasterDictionary):
    output_dict = {}
    for url_id,  filter_words in filter_data.items():
        Positive_Score = 0
        Negative_Score = 0
        text = text_data[url_id]
        for word in filter_words:
            if word in MasterDictionary['positive-words']:
                Positive_Score += 1 
            elif word in MasterDictionary['negative-words']:
                Negative_Score -= 1

        #Extracting Derived variables
        Negative_Score = abs(Negative_Score)
        Polarity_Score = (Positive_Score - Negative_Score) / ((Positive_Score + Negative_Score) + 0.000001)

        Total_words_after_cleaning = len(filter_words)
        Subjectivity_Score = (Positive_Score + Negative_Score)/ ((Total_words_after_cleaning) + 0.000001)

        Average_sentence_length = avg_sentence_length(text)

        #complex word count
        complex_words = complex_word_count(filter_words)

        #WORD COUNT
        word_count = len(filter_words)

        #Percentage of Complex words
        Percentage_of_Complex_words = (complex_words/word_count)*100

        #FOG INDEX
        Fog_Index = 0.4 * (Average_sentence_length + Percentage_of_Complex_words) 

        #SYLLABLE PER WORD
        syllable_count = syllable_count_per_word(filter_words)

        #PERSONAL PRONOUNS
        Personal_pronouns = personal_pronouns(text)

        #Average Word Length
        word_length_list = [len(word) for word in filter_words]
        avg_word_length = sum(word_length_list)/ word_count
                
        output_dict[url_id]= {'POSITIVE SCORE': Positive_Score, 'NEGATIVE SCORE': Negative_Score, 'POLARITY SCORE': Polarity_Score, 'SUBJECTIVITY SCORE': Subjectivity_Score,
                              'AVG SENTENCE LENGTH': Average_sentence_length,'PERCENTAGE OF COMPLEX WORDS': Percentage_of_Complex_words,'FOG INDEX': Fog_Index,'AVG NUMBER OF WORDS PER SENTENCE': Average_sentence_length, 'COMPLEX WORD COUNT': complex_words,
                              'WORD COUNT': word_count,'SYLLABLE PER WORD': syllable_count,'PERSONAL PRONOUNS': Personal_pronouns,'AVG WORD LENGTH': avg_word_length}
    return output_dict

def main():
    input_dir = os.path.join(os.getcwd(), "Input")

    # Load the stopwords
    stopwords_folder_path = os.path.join(input_dir, 'StopWords')
    load_stop_words_list = load_stopwords_from_folder(stopwords_folder_path)
    load_stop_words = set([word.lower() for word in load_stop_words_list])

    # NLTK predefined stopwords
    stop_words = set(stopwords.words('english'))

    # Filter the articles
    article_folder_path = os.path.join(os.getcwd(), 'article_data')
    data = filter_text_data(article_folder_path, load_stop_words, stop_words)
    filter_data = data[0]
    text_data = data[1]

    # Filter Master Dictionary
    MasterDictionary_folder_path = os.path.join(input_dir, 'MasterDictionary')
    MasterDictionary = filter_master_dictionary(MasterDictionary_folder_path, load_stop_words)

    # Output Data
    output_data_dict = output_dict(text_data, filter_data, MasterDictionary)

    # Output DataFrame
    output_df = create_output_df(output_data_dict)

    # Export to Excel
    export_to_excel(output_df)

if __name__ == "__main__":
    main()