def wiki_covid_lockdown (source = "https://en.wikipedia.org/wiki/COVID-19_pandemic_lockdowns",
                        rtrn_tbl = 'both',
                        search_tbl_class = 'default'):

    ## Adapted from 'https://simpleanalytical.com/how-to-web-scrape-wikipedia-python-urllib-beautiful-soup-pandas' ##
    
    import wikipedia
    import requests
    from bs4 import BeautifulSoup
    import numpy as np
    import re
    import pandas as pd
    from datetime import datetime
        
    ## Conditionally use local file (if containing .html extension) or live pull from Wikipedia (if no .html extension) ## 
    
    #  Read in HTML as text  #
    
    #  (Get runtime info to report -- inserted into 'F' objects below) #
    
    run_time =datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if '.html' in source.lower():
      html_doc = open(
      source,
      'r', encoding='utf-8')
    else:
      html_doc = requests.get(
      source
      ).text

    ## Use Beautiful Soup to parse HTML text and find tables ##
    
    #  Set table class to search for, if not set to 'default' #
    
    if search_tbl_class.lower() == 'default':
        if '.html' in source.lower():
            search_tbl_class = 'wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible'
        else:
            search_tbl_class = 'wikitable sortable mw-collapsible'
        
    soup = BeautifulSoup(html_doc, 'html.parser')
    right_tables = soup.findAll('table', class_ = search_tbl_class)

    ## Create list objects to hold column values ##
    
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]

    ## Loop through table rows with 'tr' tags and posit values from 'td' within the correct column position ##
    ## depending on number of cells in the 'td' object. ##
    
    for row in right_tables[0].findAll('tr'):
        cells=row.findAll('td')
        if len(cells)==3 and cells[0].findAll('img') != []:
            mlnk=cells[0].findAll('a')
            A.append(mlnk[0].contents[0])
            B.append('NA')
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            E.append('NA')
        elif len(cells)==3 and cells[0].findAll('img') == []:
            A.append('NA')
            mlnk=cells[0].findAll('a')
            B.append(mlnk[0].contents[0])
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            E.append('NA')
        if len(cells)==4 and cells[0].findAll('img') != []:
            mlnk=cells[0].findAll('a')
            A.append(mlnk[0].contents[0])
            B.append('NA')
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            E.append(cells[3].find(text=True))
        elif len(cells)==4 and cells[0].findAll('img') == []:
            A.append('NA')
            mlnk=cells[0].findAll('a')
            B.append(', '.join(map(str, [x.contents[0] for x in mlnk])))
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            E.append(cells[3].find(text=True))
        if len(cells)==5:
            mlnk=cells[0].findAll('a')
            A.append(mlnk[0].contents[0])
            B.append(cells[1].find(text=True))
            C.append(cells[2].find(text=True))
            D.append(cells[3].find(text=True))
            E.append(cells[4].find(text=True))

    ## Clean up a little ##
            
    for i in range(len(A)):
      A[i] = re.sub("<i>|</i>", "", str(A[i]))
      if A[i] == 'NA':
        A[i] = A[i - 1]
      if D[i] == '\n':
        D[i] = 'NA'
      E[i] = re.sub("\n", "", E[i])
      if E[i] == 'NA':
        E[i] = E[i - 1]

    ## Add timestamp and indiaction of local or web data pull ##
        
    if  '.html' in source.lower():
      F_lock = [run_time + '_local' for x in range(i + 1)]
    else:
      F_lock = [run_time + '_web' for x in range(i + 1)]

    ## Scrape No lockdown order table ## 

    G = []
    H = []

    for row in right_tables[1].findAll('tr'):
        cells2=row.findAll('td')
        if len(cells2) == 1:
          G.append('NA')
          H.append(cells2[0].find(text=True))
        if len(cells2) == 2:
          mlnk=cells2[0].findAll('a')
          G.append(mlnk[0].contents[0])
          # H.append(cells2[1].find(text=True))
          H.append('NA')
        if len(cells2) == 3:
          mlnk=cells2[0].findAll('a')
          G.append(mlnk[0].contents[0])
          H.append(cells2[1].find(text=True))

    if  '.html' in source.lower():
      F_no_lock = [run_time + '_local' for x in range(len(G))]
    else:
      F_no_lock = [run_time + '_web' for x in range(len(G))]

    df_lock=pd.DataFrame(A,columns=['Countries and territories'])
    df_lock['Place']=B
    df_lock['Start date']=C
    df_lock['End date']=D
    df_lock['Level']=E
    df_lock['HTML_TYPE']=F_lock
    df_lock

    df_no_lock=pd.DataFrame(G,columns=['Countries and territories'])
    df_no_lock['Place']=H
    df_no_lock['HTML_TYPE']=F_no_lock
    df_no_lock

    if rtrn_tbl.lower() == 'locked':
        return df_lock
    elif rtrn_tbl.lower() == 'not_locked':
        return df_no_lock
    else:
        return df_lock, df_no_lock
    

