from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np

# # # LOOP OVER ALL ARTICLES STARTS HERE # # #
# get article and turn into BeautifulSoup object
page = """C:/Users/Antoine/Desktop/JNP html articles/2011/1/Landomycins P−W, Cytotoxic Angucyclines from Streptomyces cyanogenus S-136   Journal of Natural Products.html"""
html_file = open(page, encoding='utf-8-sig')
soup = BeautifulSoup(html_file, 'html.parser')

# removing links and bolded text tags, and their contents
for b in soup('b'):
    b.decompose()
div = soup.find('div')
# print(div.prettify())

########################################################################################################################
# # # List of all NMR table titles # # #
table_titles = div.find_all('div', class_='NLM_caption')
table_titles = [ele.text.strip() for ele in table_titles]
table_titles = [ele.replace(" ()", "") for ele in table_titles]
table_titles = [ele.replace("/", " ") for ele in table_titles]                                                          # un-separated list of NMR table titles

########################################################################################################################
# finds DOI, article title, year, and combines them into a string csv_file_name [had to shorten to just DOI]
html_file = open(page, encoding='utf-8-sig')
soup = BeautifulSoup(html_file, 'html.parser')
div = soup.find('div')
DOILink = div.find('div', class_='article_header-doiurl').a.text
DOIFileName1 = os.path.split(os.path.dirname(DOILink))[1]
DOIFileName2 = os.path.split(DOILink)[1]
DOI = str(DOIFileName1 + "-" + DOIFileName2)

title = div.find('div', class_='article_header-left pull-left').h1.span.text
print(title)
year = div.find('ul', class_='rlist article-chapter-history-list').text
year = str(year)
year = year[-4:]

csv_file_name = str(title + "; " + year + "; " + DOI)

########################################################################################################################
# # # FUNCTION TO CREATE NEW FOLDERS CONTAINING NEW CSV FILES # # #
# creates new directory; returns directory path
def folder_path():
    parent_dir = "C:/Users/Antoine/Desktop/2011"
    directory = DOI
    path = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path)
    except:
        pass

    return path

########################################################################################################################
# # # Headers, Footnotes, Miscellaneous data  # # #
headers = div.find_all('th', class_='colsep0 rowsep0')
headers = [ele.text.strip() for ele in headers]
headers = [ele.replace(" ()", " ") for ele in headers]

footnotes = div.find_all('div', class_="footnote")
footnotes = [ele.text.strip() for ele in footnotes]

temp_headers = []
rest_headers = headers
temp_footnotes = []
rest_footnotes = footnotes
temp_data = []
previous_i = 0
previous_j = 0
start = 0
final_headers = []
count = 0
header_3 = str('')
previous_item = 0
data = [[csv_file_name]]
list_of_lists_headers1 = []
list_of_lists_headers2 = []
list_of_lists_headers3 = []

########################################################################################################################
# split footnotes list into new separate lists for each NMR table, then combine into a list of lists for appending later
for i, footnote in enumerate(footnotes):
    if i > 0 and footnote.startswith('a') or i == (len(footnotes) - 1):
        temp_footnotes = footnotes[previous_i:i]
        rest_footnotes = rest_footnotes[i:]
        if i == (len(footnotes) - 1):
            temp_footnotes = footnotes[previous_j:]
        previous_i = i
        list_of_lists_headers3 += [temp_footnotes]

for j, header in enumerate(headers):                                                                                    # split headers list into new separate lists headers for each NMR table
    if j > 0 and header == '' or header.startswith('sugar') or j == (len(headers) - 1):
        temp_headers = headers[previous_j:j]
        rest_headers = rest_headers[j:]
        if j == (len(headers) - 1):
            temp_headers = headers[previous_j:]
        previous_j = j                                                                                                  # previous final index for temp_header
        for l, temp_header in enumerate(temp_headers):
            if temp_header == "position":
                header_1 = temp_headers[0:l]
                header_2 = temp_headers[l:]
                list_of_lists_headers1 += [header_1]
                list_of_lists_headers2 += [header_2]
                count += 1

count = 0
# # # LOOP OVER ALL NMR TABLES STARTS HERE # # #
for row in div.find_all('tr'):
    columns = row.find_all('td')
    columns = [ele.text.strip() for ele in columns]
    if columns == []:                                                                                                   # Pycharm suggests replace to "if not" but this is not equivalent,
        if previous_item == []:                                                                                         # it breaks code at line 146 with "IndexError: list index out of range"
            data.append(["---------------------------------------------------------------------------------------------------------------------------------------------------------------------"])
            table_title = [f"{table_titles[count]}"]
            footnote = ["Footnotes: " + f"{list_of_lists_headers3[count]}"]
            data.append(table_title)
            data.append(footnote)
            data.append("")
            data.append(list_of_lists_headers1[count])
            data.append(list_of_lists_headers2[count])
            count += 1
            continue
    previous_item = columns
    data.append(columns)

print(data)
dftable = pd.DataFrame(data)
# print(dftable)

# # # Create CSV files for each NMR Table # # #
csv_path = folder_path() + f"/{title}.csv"
dftable.to_csv(csv_path, index=False, header=False, encoding='utf-8-sig')

########################################################################################################################
# # # Replace a,b,c,etc hyperlink in headers with table footnotes # # #
# for i, temp_header in enumerate(headers):                                                                             # replacing superscripts in headers with their footnotes
#     if i > 0 and temp_header == '' or temp_header.startswith('sugar') or i == (len(headers) - 1):
#         temp_headers = headers[previous_i:i]
#         rest_headers = rest_headers[i:]
#         if i == (len(headers) - 1):
#             temp_footnotes = footnotes[previous_i:]
#         previous_i = i                                                                                                  # previous final index for temp_footnotes
#         print(temp_headers)
#         for j, footnote in enumerate(footnotes):
#             if footnote.startswith('a') or j == (len(footnotes) - 1):
#                 temp_footnotes = footnotes[start:j]
#                 rest_footnotes = rest_footnotes[j:]
#                 if j == (len(footnotes) - 1):
#                     temp_footnotes = footnotes[start:]
#                 start = j                                                                                               # previous final index for temp_footnotes
#                 if not temp_footnotes: continue                                                                         # was printing out an empty list; tried to fix, gave up so used continue instead
#                 # print(temp_footnotes)
#                 for k, temp_footnote in enumerate(temp_footnotes):                                                      # assign footnotes to variables, to be merged with headers later
#                     if temp_footnote.startswith('a'): a = (temp_footnotes[0])[1:-1]                                     # [1:-1] range removes footnote letter and end dot
#                     elif temp_footnote.startswith('b'): b = (temp_footnotes[1])[1:-1]
#                     elif temp_footnote.startswith('c'): c = (temp_footnotes[2])[1:-1]
#                     elif temp_footnote.startswith('d'): d = (temp_footnotes[3])[1:-1]
#                     elif temp_footnote.startswith('e'): e = (temp_footnotes[4])[1:-1]
#                     elif temp_footnote.startswith('f'): f = (temp_footnotes[5])[1:-1]
#                 # for m, temp_header in enumerate(headers):                                                             # replacing superscripts in headers with their footnotes
#                     # if m > 0 and temp_header.startswith(""): continue  ##START NEW LOOP FOR NEXT TABLE, NEW FOOTNOTES##       !!! START NEW LOOP FOR NEW TABLE!!!
#         if temp_header.endswith('a'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + a + ')'
#         elif temp_header.endswith('b'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + b + ')'
#         elif temp_header.endswith('c'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + c + ')'
#         elif temp_header.endswith('d'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + d + ')'
#         else:
#             final_headers.append(temp_header)
#         final_headers.append(temp_header)
#
# print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////")
# print()
# print(final_headers)                                                                                                    # !!!!! PROBLEMS HERE !!!!!!
# print()
# print(headers)
# print(footnotes)
# print(final_headers)
########################################################################################################################

# headers = div.find_all('th', class_='colsep0 rowsep0')
# headers = [cell.text.strip() for cell in headers]
# headers = [cell.replace(" ()", "") for cell in headers]
# print(headers)

# TO-DO:
    # title: table_title for each different table from table_titles list
    # number of elements in table_titles equals total number of NMR tables equals total CSV files to create
    # split table_titles list into several different strings
    # [X] footnotes: split list into several smaller lists; assign variables a=footnotes[0]
    # headers: headers for each different table
        # [X] figure out how to split "headers" list
        # [X] footnotes: for each NMR table, replace headers hyperlink a,b,c,etc. with footnote at end of table
        # [X] dictionary of alphabet letters linked to elements in temp_headers
        # don't replace superscripts with footnotes, instead print both as 1st and 2nd table header lines
    # fill columns and rows of a csv, each cell comma-separated
    # separate different tables (new csv/table)
    # if/else: create new csv only if table_title contains "NMR"
    # add csv_file_name for each article as it is looped over, to a txt file
