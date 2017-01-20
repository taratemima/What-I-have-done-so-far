import save_results_in_cvs_file
import FrequencySummarizer as fs

def testing_length(file_name):
    search_term = 'abstract'
    doc_root = save_results_in_cvs_file.create_tree(file_name)

    new_text = ""

    for match in doc_root.findall(search_term):
        original_text = match.text
        if original_text.count(' ') > 1000:
            new_text = fs.summarize(original_text, 1)
        else:
            new_text = original_text
    return new_text
