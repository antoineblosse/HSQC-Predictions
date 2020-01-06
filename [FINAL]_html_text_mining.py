from bs4 import BeautifulSoup
import pandas as pd
import os

month = "1"                                                                                                             # start in january
directory = "C:/Users/Antoine/Desktop/JNP html articles/2018/" + month
# # # LOOP OVER ALL ARTICLES STARTS HERE # # #
for root, dirs, files in os.walk(directory, topdown=True):
    for file in files:
        page = directory + "/" + file
        html_file = open(page, encoding='utf-8-sig')                                                                    # get article and turn into BeautifulSoup object
        soup = BeautifulSoup(html_file, 'html.parser')
        div = soup.find('div')

        ################################################################################################################
        # # # List of all NMR table titles # # #
        table_titles = div.find_all('div', class_='NLM_caption')
        table_titles = [ele.text.strip() for ele in table_titles]
        table_titles = [ele.replace(" ()", "") for ele in table_titles]
        table_titles = [ele.replace("/", " ") for ele in table_titles]                                                  # un-separated list of NMR table titles
        table_titles = [ele.replace(":", "") for ele in table_titles]
        table_titles = [ele.replace("*", "") for ele in table_titles]
        table_titles = [ele.replace("?", "") for ele in table_titles]
        table_titles = [ele.replace(">", "") for ele in table_titles]
        table_titles = [ele.replace("<", "") for ele in table_titles]

        ################################################################################################################
        # finds DOI, article title, year, and combines them into a string csv_file_name [had to shorten to just DOI]
        html_file = open(page, encoding='utf-8-sig')
        soup = BeautifulSoup(html_file, 'html.parser')
        div = soup.find('div')
        DOILink = div.find('div', class_='article_header-doiurl').a.text
        DOIFileName1 = os.path.split(os.path.dirname(DOILink))[1]
        DOIFileName2 = os.path.split(DOILink)[1]
        DOI = str(DOIFileName1 + "-" + DOIFileName2)
        article_title = div.find('div', class_='article_header-left pull-left').h1.span.text
        year = div.find('ul', class_='rlist article-chapter-history-list').text
        year = str(year)
        year = year[-4:]
        article_and_doi = str("Article: " + article_title + "; " + year + "; " + DOI)

        ################################################################################################################
        # # # FUNCTION TO CREATE NEW FOLDERS CONTAINING NEW CSV FILES # # #
        # creates new directory; returns directory path
        def folder_path():
            parent_dir = "C:/Users/Antoine/Desktop/2018/" + month
            directory = DOI
            path = os.path.join(parent_dir, directory)
            try:
                os.makedirs(path)
            except: pass
            return path


        ################################################################################################################
        # # # Headers, Footnotes, Miscellaneous data  # # #
        headers_row1 = div.find_all('th', class_=['rowsep1 colsep0'])                                                   # first nmr table header row
        headers_row1 = [ele.text.strip() for ele in headers_row1]
        headers_row1 = [ele.replace(" ()", " ") for ele in headers_row1]

        headers_row2 = div.find_all('th', class_=['colsep0 rowsep0'])                                                   # second nmr table header row
        headers_row2 = [ele.text.strip() for ele in headers_row2]
        headers_row2 = [ele.replace(" ()", " ") for ele in headers_row2]

        footnotes = div.find_all('div', class_="footnote")
        footnotes = [ele.text.strip() for ele in footnotes]

        temp_headers = []
        rest_headers = headers_row2
        temp_footnotes = []
        rest_footnotes = footnotes
        temp_data = []
        previous_i = 0
        previous_j = 0
        start = 0
        final_headers = []
        count = 0
        header_3 = str('')
        previous_row = 0
        earlier_row = 0
        list_of_lists_headers1 = []
        list_of_lists_headers2 = []
        list_of_lists_headers3 = []

        ################################################################################################################
        for i, footnote in enumerate(footnotes):                                                                        # split footnotes list into new separate lists for each NMR table, then combine into a list of lists for appending later
            if i > 0 and footnote.startswith('a') or i == (len(footnotes) - 1):
                temp_footnotes = footnotes[previous_i:i]
                rest_footnotes = rest_footnotes[i:]
                if i == (len(footnotes) - 1):
                    temp_footnotes = footnotes[previous_j:]
                previous_i = i
                list_of_lists_headers3 += [temp_footnotes]

        synonyms = ("position", "positiona", "atom", "no.", "sample", "compound", "compd", "compound 1a", "compoundb", "entry", "organism")

        for j, header in enumerate(headers_row2):                                                                       # split headers list into new separate lists headers for each NMR table
            if j > 0 and ((header == '') or (header in synonyms) or (j == (len(headers_row2) - 1))):
                temp_headers = headers_row2[previous_j:j]
                if j == (len(headers_row2) - 1):
                    temp_headers = headers_row2[previous_j:]
                previous_j = j                                                                                          # previous final index for temp_header
                if temp_headers == ['']:
                    continue
                if temp_headers[0] == '':
                    temp_headers = temp_headers[1:]
                list_of_lists_headers2 += [temp_headers]

        if list_of_lists_headers1 == [] and list_of_lists_headers2 == [] and list_of_lists_headers3 == []:
            print("No NMR table in article")
            continue

        data = [[article_and_doi], [""], [""]]                                                                          # create first nmr table
        try:
            table_title = [f"{table_titles[count]}"]
            data.append(table_title)
        except: data.append(["Table Title not found"])
        try:
            footnote = ["Footnotes: " + f"{list_of_lists_headers3[count]}"]
            data.append(footnote)
        except: pass
        data.append("")
        try:
            data.append(list_of_lists_headers2[count])
        except: data.append(["position"])
        count += 1                                                                                                      # count +1 each time NMR table headers/footnotes are added, count value at the end of entire loop is total number of NMR tables created

        # # LOOP OVER ALL NMR TABLES STARTS HERE # # #
        for row in div.find_all('tr'):
            current_row = row.find_all('td')
            current_row = [ele.text.strip() for ele in current_row]
            # print(current_row)
            if current_row == []:                                                                                       # Pycharm suggests replace to "if not current_row" but this is not equivalent, it breaks code at line 146 with "IndexError: list index out of range
                if previous_row == [] or earlier_row == [] or current_row == div.find_all('tr')[-1]:
                    continue
                elif previous_row is not 0:                                                                             # Create CSV files for each NMR Table
                    dftable = pd.DataFrame(data)
                    try:                                                                                                # try/except to catch index errors
                        if len(table_titles[(count-1)]) > 120:
                            table_titles[(count-1)] = table_titles[(count-1)][0:120]
                        csv_path = folder_path() + f"/{table_titles[(count-1)]}.csv"
                    except:
                        print("! ERROR: " + article_and_doi)
                        try:
                            if len(table_titles[(count-2)]) > 120:
                                table_titles[(count-2)] = table_titles[(count-2)][0:120]
                            csv_path = folder_path() + f"/{table_titles[(count-2)]}.csv"
                        except: pass
                    dftable.to_csv(csv_path, index=False, header=False, encoding='utf-8-sig')
                    data = [[article_and_doi], [""], [""]]                                                              # reset data list
                    try:
                        table_title = [f"{table_titles[count]}"]
                        data.append(table_title)
                    except: data.append(["Table Title not found"])
                    try:
                        footnote = ["Footnotes: " + f"{list_of_lists_headers3[count]}"]
                        data.append(footnote)
                    except: pass
                    data.append("")
                    try:
                        data.append(list_of_lists_headers2[count])
                    except: data.append(["position"])
                    count += 1
            else:
                data.append(current_row)
            earlier_row = previous_row
            previous_row = current_row

        if len(table_titles[-1]) > 120:
            table_titles[-1] = table_titles[-1][0:120]
        dftable = pd.DataFrame(data)
        csv_path = folder_path() + f"/{table_titles[-1]}.csv"
        dftable.to_csv(csv_path, index=False, header=False, encoding='utf-8-sig')
