import os


def compare_content(test_file_path, content):
    with open(test_file_path, 'r') as file1:
        test_content = file1.read()

        if content == test_content:
            return True
        else:
            return False

# # Usage example
# file1_path = 'file1.txt'
# file2_path = 'file2.txt'
# if compare_files(file1_path, file2_path):
#     print("The files have the same content.")
# else:
#     print("The files have different content.")


# write function to extract problematic bylines

def extract_byline(soup):
    selectors = [
        '.byline',  # Example CSS class selector
        '#author',  # Example ID selector
        'span[data-role="author"]',  # Example attribute selector
        'a[data-qa="author-name"]',  # Example attribute selector
        'p > a.Byline-author',  # Example descendant selector
        'a[class*=byline]',
        'span[class*=byline]',
        'div[class*=byline]'
    ]

    res = []
    html = ""
    for selector in selectors:
        res.append(soup.css.select(selector))

    for result in res:
        if len(result) > 0:
            for e in result:
                html += e.get_text(separator=' ', strip=True) + ' '

    return html


def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None


# extract body content properly

# it's useless'
def justify_text(text):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)

    justified_lines = []
    for line in lines:
        padding = max_length - len(line)
        words = line.split()
        num_words = len(words)
        if num_words > 1:
            space_count = padding // (num_words - 1)
            extra_spaces = padding % (num_words - 1)
            justified_line = words[0] + ' ' * space_count
            for i in range(1, num_words):
                if extra_spaces > 0:
                    justified_line += ' '
                    extra_spaces -= 1
                justified_line += ' ' * space_count + words[i]
        else:
            justified_line = line
        justified_lines.append(justified_line)

    return '\n'.join(justified_lines)
