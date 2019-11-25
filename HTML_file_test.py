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
# for a in soup('a'):
#     a.decompose()
div = soup.find('div')
# print(div.prettify())


########################################################################################################################
# # # FUNCTION TO CREATE NEW FOLDERS CONTAINING NEW CSV FILES # # #
# 1st: finds DOI, article title, year, and combines them into a string csv_file_name [had to shorten to just DOI]
# 2nd: creates new directory; returns directory path
def create_folders():
    html_file = open(page, encoding='utf-8-sig')
    soup = BeautifulSoup(html_file, 'html.parser')
    div = soup.find('div')
    DOILink = div.find('div', class_='article_header-doiurl').a.text
    DOIFileName1 = os.path.split(os.path.dirname(DOILink))[1]
    DOIFileName2 = os.path.split(DOILink)[1]
    DOI = str(DOIFileName1 + "-" + DOIFileName2)

    title = div.find('div', class_='article_header-left pull-left').h1.span.text

    year = div.find('ul', class_='rlist article-chapter-history-list').text
    year = str(year)
    year = year[-4:]

    csv_file_name = str(year + "; " + title + "; " + DOI)

    parent_dir = "C:/Users/Antoine/Desktop/2011"
    directory = DOI
    path = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path)
    except:
        pass

    return path
########################################################################################################################


########################################################################################################################
# # # List of all NMR table titles # # #
table_titles = div.find_all('div', class_='NLM_caption')
table_titles = [ele.text.strip() for ele in table_titles]
table_titles = [ele.replace(" ()", "") for ele in table_titles]
table_titles = [ele.replace("/", " ") for ele in table_titles]                                                          # un-separated list of NMR table titles

# n = len(table_titles)                                                                                                   # number of csv files to create
########################################################################################################################

########################################################################################################################
# # # Headers, Footnotes, Miscellaneous data  # # #
headers = div.find_all('th', class_='colsep0 rowsep0')
headers = [ele.text.strip() for ele in headers]
headers = [ele.replace(" ()", " ") for ele in headers]
# print(headers)

footnotes = div.find_all('div', class_="footnote")
footnotes = [ele.text.strip() for ele in footnotes]
# print(footnotes.prettify())
# print(footnotes)
# print()
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
########################################################################################################################


################################################  TESTING  #############################################################
testing_data = []

# for n in range(len(table_titles)):
for i, header in enumerate(headers):                                                                           # split headers list into new separate lists headers for each NMR table
    if i > 0 and header == '' or header.startswith('sugar') or i == (len(headers) - 1):
        temp_headers = headers[previous_i:i]
        rest_headers = rest_headers[i:]
        if i == (len(headers) - 1):
            temp_headers = headers[previous_i:]
        previous_i = i                                                                                                  # previous final index for temp_header
        testing_data.append(temp_headers)
        print(temp_headers)
        for l, temp_header in enumerate(temp_headers):
            if temp_header == "position":
                header_1 = temp_headers[0:l]
                header_2 = temp_headers[l:]
                print(header_1)
                print(header_2)
                print()
        # print(temp_headers)
for j, footnote in enumerate(footnotes):                                                                           # split footnotes list into new separate lists for each NMR table
    if j > 0 and footnote.startswith('a') or j == (len(footnotes) - 1):
        temp_footnotes = footnotes[previous_j:j]
        rest_footnotes = rest_footnotes[j:]
        if j == (len(footnotes) - 1):
            temp_footnotes = footnotes[previous_j:]
        previous_j = j
        # print(temp_footnotes)
        # for temp_footnote in temp_footnotes:
        #     header_3 += " " + str(temp_footnote)
        testing_data.append(temp_footnotes)
        # testing_data.append(header_3)
        # header_3 = str('')

testing_data.append("")
testing_data.append("ayyy lmao")
# print(header_3)
# print(testing_data)
dftable = pd.DataFrame(testing_data)
# print(dftable)

########################################################################################################################
# # # Get all tables in article, even non-NMR # # #
# for tr in div.find_all('tr'):
#     row = tr.text
#     tds = tr.find_all('td')
#     tds = tds.text
#     print(row)
#     for column in row:
#         cell = []
#         print(cell)

# rows = soup.find_all('tr')
# print(rows)
# NMRTableHeader1 = div.find('tr', class_='colsep0').text
# print(NMRTableHeader1)
data = []
data_with_headers = []

# # # LOOP OVER ALL NMR TABLES STARTS HERE # # #
for row in div.find_all('tr'):
    # print(row)
    # # # need to print headers before data
    # if "class == 'colsep0'" in row:
    #     header = div.find_all('tr', class_='colsep0')
    #     print(header)
    #     data_with_headers.append(header)
    # else:
    #     continue
    # for header in div.find_all('th'):
    #     header = header.text
    #     # header = [ele.text.strip() for ele in header]
    #     print(header)
    # headers = div.find_all('th', class_='colsep0 rowsep0')
    # headers = [ele.text.strip() for ele in headers]
    # print(header)
    # data.append(header)
    # if header is None:
    #     break
    # else:
    #     header = [ele.text.strip() for ele in header]
    #     data.append(ele for ele in header if ele)  # Get rid of empty values)
    #     # print(header)
    columns = row.find_all('td')
    columns = [ele.text.strip() for ele in columns]
    if not columns:
        if count == 0: pass
        header_1 = ['', 'landomycin P a', 'landomycin Q a', 'landomycin R a']
        header_2 = ['position', 'δCb,c', 'δH (500 MHz)b', 'δH (500 MHz)b', 'δH (500 MHz)d']
        header_3 = ['aSee also Figures S13−S18.', 'bCDCl3.', 'c125 MHz.', 'dDMSO-d6.', 'eNot observed.']
        data.append(header_1)
        data.append(header_2)
        data.append(header_3)
    data.append(columns)
    count += 1
    # cols = row.find_all('tr')
    # # cols = [ele.text.strip() for ele in columns]
    # data_with_headers.append(cols)

# print()
# print(data)
# dftable = pd.DataFrame(data)
# print(dftable)

# for m, header in enumerate(headers):
#     headers[m] = header.replace(" ()", "")
    # n_lists = headers.count("")         # temporary replacement for table_title[i]
    # for n in range(n_lists):
    #     split_headers = headers.split("")
#     # parts = headers.split('')
#     # print(parts)
#     if header == "":
#         print('ok')
#         np.split(headers, [0, i])
# print(n_lists)

# print(headers)
# print()


# # # split footnotes list into smaller lists, one for each NMR table
# for m, header in enumerate(headers):
#     if m > 0 and header == '' or m == (len(headers) - 1):
#         temp_headers = headers[previous_i:m]
#         rest_headers = rest_headers[m:]
#         if m == (len(headers) - 1):
#             temp_footnotes = footnotes[previous_i:]
#         previous_i = m                                                                                                  # previous final index for temp_footnotes
#         print(temp_headers)
#         for j, footnote in enumerate(footnotes):
#             if j > 0 and footnote.startswith('a') or j == (len(footnotes) - 1):
#                 temp_footnotes = footnotes[start:j]
#                 rest_footnotes = rest_footnotes[j:]
#                 if j == (len(footnotes) - 1):
#                     temp_footnotes = footnotes[start:]
#                 start = j                                                                                               # previous final index for temp_footnotes
#                 # print(temp_footnotes)                             #################
#                 # print()
#                 superscripts = {}                                                                                       # create dictionary for superscript/footnote pairs
#                 # keys = range(len(alphabet))
#                 # for k in keys:
#                 #     superscripts[1] = (alphabet[1], temp_footnotes[1])
#                 # print(superscripts)
#                 # for n in len(temp_footnotes):
#                 #     alphabet[n] = temp_footnotes[n]
#                 #     print(alphabet)
#                 for n, temp_header in enumerate(temp_headers):                                                          # replacing superscripts in headers with their footnotes
#                     if temp_header.endswith('a'):
#                         temp_header = temp_header[:-1]
#                         # temp_a = temp_footnotes[0]
#                         temp_a = '250MHz'
#                         temp_header = temp_header + ' (' + temp_a + ')'
#                         # print(temp_header)
#                         # temp_headers[n] = temp_header
########################################################################################################################

########################################################################################################################
# # # Split headers/footnotes list into new separate lists for each table; use both as 1st & 2nd table header lines in CSV
for i, header in enumerate(headers):                                                                               # split headers list into new separate lists headers for each NMR table
    if i > 0 and header == '' or header.startswith('sugar') or i == (len(headers) - 1):
        temp_headers = headers[previous_i:i]
        rest_headers = rest_headers[i:]
        if i == (len(headers) - 1):
            temp_headers = headers[previous_i:]
        previous_i = i                                                                                                  # previous final index for temp_header
        # print(temp_headers)

for j, footnote in enumerate(footnotes):                                                                           # split footnotes list into new separate lists for each NMR table
    if j > 0 and footnote.startswith('a') or j == (len(footnotes) - 1):
        temp_footnotes = footnotes[previous_j:j]
        rest_footnotes = rest_footnotes[j:]
        if j == (len(footnotes) - 1):
            temp_footnotes = footnotes[previous_j:]
        previous_j = j                                                                                                  # previous final index for temp_footnotes
        # print(temp_footnotes)

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
#         elif temp_header.endswith('e'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + e + ')'
#         elif temp_header.endswith('f'):
#             temp_header = temp_header[:-1]
#             temp_header = temp_header + ' (' + f + ')'
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
# # # Create CSV files for each NMR Table # # #
csv_path = create_folders() + f"/{table_titles[0]}.csv"
dftable.to_csv(csv_path, index=False, header=True, encoding='utf-8-sig')
# dftable.to_csv(csv_path, header=True, columns=headers, encoding='utf-8-sig')
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
