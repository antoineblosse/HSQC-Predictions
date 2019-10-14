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
for a in soup('a'):
    a.decompose()
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
    # # need to print headers before data
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
    headers = div.find_all('th', class_='colsep0 rowsep0')
    headers = [ele.text.strip() for ele in headers]
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

# print(data)
dftable = pd.DataFrame(data)
# print(dftable)


# # # First NMR Table
table_title = div.find('div', class_='NLM_caption').text
table_title = table_title.replace("/", " ")
table_title = table_title.replace(" ()", "")

########################################################################################################################
# # # Create CSV files for each NMR Table # # #
csv_path = create_folders() + f"/{table_title}.csv"
dftable.to_csv(csv_path, header=True, encoding='utf-8-sig')
########################################################################################################################

# headers = div.find_all('th', class_='colsep0 rowsep0')
# headers = [cell.text.strip() for cell in headers]
# headers = [cell.replace(" ()", "") for cell in headers]
# for header in headers:
#     if header == "":
#         np.split(headers)
# print(headers)

# TO-DO:
    # need to fill columns and rows of a csv, each cell comma-separated
    # headers for each different table
    # separate different tables (new csv/table)
