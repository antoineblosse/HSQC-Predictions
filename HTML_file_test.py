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
# table_body = table.find('tbody')

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
    data.append(columns)
    # cols = row.find_all('tr')
    # # cols = [ele.text.strip() for ele in columns]
    # data_with_headers.append(cols)

# print()
# print(data)
# dftable = pd.DataFrame(data)
# print(dftable)

# # # if last letter in header string is a,b,c,d,e; replace with text in footnotes  # # #
headers = div.find_all('th', class_='colsep0 rowsep0')
headers = [ele.text.strip() for ele in headers]
# print(headers)

for i, header in enumerate(headers):
    headers[i] = header.replace(" ()", "")
    n_lists = headers.count("")         # temporary replacement for table_title[i]
    # for n in range(n_lists):
    #     split_headers = headers.split("")
#     # parts = headers.split('')
#     # print(parts)
#     if header == "":
#         print('ok')
#         np.split(headers, [0, i])
# print(n_lists)


# print()
# print(headers)

header1 = headers[1]
if header1.endswith(('a', 'b', 'c', 'd')):
    header1 = header1[:-1]
    header1 = header1 + " (125 MHz)"
# print(header1)


footnotes = div.find_all('div', class_="footnote")
footnotes = [ele.text.strip() for ele in footnotes]
# print(footnotes.prettify())
print(footnotes)
print()
temp_headers = []
temp_footnotes = []
rest_footnotes = footnotes
temp_data = []
start = 0

# # # split footnotes list into smaller lists, one for each NMR table
# for i, header in enumerate(headers):
for i, footnote in enumerate(footnotes):
    # if i == (len(footnotes) - 1):
    #     print('+++++++++++++++')
    if i > 0 and footnote.startswith('a') or i == (len(footnotes) - 1):
        # if footnote == footnotes[0]: continue               # ignore first empty list
        # print('++++++++++' + footnote + '++++++++++++' + '  ' + str(i))
        temp_footnotes = footnotes[start:i]
        rest_footnotes = rest_footnotes[i:]
        if i == (len(footnotes) - 1):
            # print('////////')
            temp_footnotes = footnotes[start:]
        start = i                                           # previous final index for temp_footnotes
        print(temp_footnotes)
        print()
        # for i, temp_footnote in enumerate(temp_footnotes):
        #   if temp_footnotes.startswith('a') & temp_headers.endswith('a'):
        #       pass


# # # First NMR Table
table_title = div.find('div', class_='NLM_caption').text
table_title = table_title.replace("/", " ")
table_title = table_title.replace(" ()", "")

########################################################################################################################
# # # Create CSV files for each NMR Table # # #
csv_path = create_folders() + f"/{table_title}.csv"
# dftable.to_csv(csv_path, header=True, columns=headers, encoding='utf-8-sig')
########################################################################################################################

# headers = div.find_all('th', class_='colsep0 rowsep0')
# headers = [cell.text.strip() for cell in headers]
# headers = [cell.replace(" ()", "") for cell in headers]
# print(headers)

# TO-DO:
    # title: table_title for each different table
    # headers: headers for each different table
        # figure out how to split "headers" list
        # footnotes: for each NMR table, replace headers hyperlink a,b,c,etc. with footnote at end of table
    # fill columns and rows of a csv, each cell comma-separated
    # separate different tables (new csv/table)
    # if/else: create new csv only if table_title contains "NMR"
