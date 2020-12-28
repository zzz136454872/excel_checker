from openpyxl import Workbook, load_workbook
from chinese import rm_chinese
import os
import logging
from difflib import SequenceMatcher
from tools import wash_str,title2filename

class Checker:
    id_column=0
    title_column=1
    type_column=2
    author_column=3
    organization_column=4
    email_column=5
    doi_column=6
    url_column=7
    first_time_column=8
    time_column=9
    source_column=10
    volume_column=11
    issue_column=12
    page_column=13
    abstract_column=15
    keyword_column=16
    reference_column=17
    pdf_column=20
    not_doc_column=22

    header_len=21

    def __init__(self,filename,pdf_dir=None):
        self.wb=load_workbook(filename)
        self.ws=self.wb.active
        rows=list(self.ws.rows)
        self.log=logging.getLogger()
        self.log.setLevel(logging.WARNING)
        fmt=logging.Formatter('%(levelname)s: %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        self.log.addHandler(ch)
        self.pdf_dir=pdf_dir
        self.base_path=['pdf/']
        if self.pdf_dir!=None:
            if pdf_dir[-1]!='/':
                pdf_dir+='/'
            self.base_path.append(pdf_dir)
        for i in range(self.header_len,len(rows)):
            if self.void_row(rows[i]): #腾讯文档产生的空行
                break 
            if rows[i][self.not_doc_column].value!=None: #不是文献
                continue
            self.base_check([cell.value for cell in rows[i]],i+1)

    def base_check(self,row,number):
        has_error=False
        has_warning=False
        authors=row[self.author_column].split(', ')

        if row[self.organization_column]!=None:
            organizations=row[self.organization_column].split(', ')
            if len(authors)!=len(organizations):
                self.log.error('author organization mismatch')
                self.log.error(organizations)
                has_error=True

        if row[self.email_column]!=None:
            emails=row[self.email_column].split(', ')
            if len(authors)!=len(emails):
                self.log.error('error: author email mismatch')
                self.log.error(emails)
                has_error=True

        if row[self.type_column]==None:
            self.log.error('error: type void')
            has_error=True
        # elif row[self.type_column]!='Informal_Publications' and \
        #      row[self.type_column]!='White_Papers' and \
        #     row[self.doi_column]==None:
        #     self.log.warning('doi missing')
        #     has_warning=True
        if row[self.source_column]==None:
            has_error=True
            self.log.error('source missing')
        if row[self.url_column]==None:
            has_warning=True
            self.log.warning('url missing')
        if row[self.first_time_column]==None:
            has_error=True
            self.log.error('first time missing')
        if row[self.time_column]==None:
            has_error=True
            self.log.error('time missing')
        if row[self.abstract_column]==None and \
             row[self.type_column]!='White_Papers':
            self.log.warning('abstract missing')
            has_warning=True
        if row[self.reference_column]==None and \
             row[self.type_column]!='White_Papers':
            self.log.warning('reference missing')
            has_warning=True
        if row[self.pdf_column]==None:
            self.log.warning('no pdf found')
            has_warning=True
        else:
            title=row[self.title_column]
            gen_name=title2filename(wash_str(title),'.pdf')
            if self.pdf_dir!=None:
                if self.direct_pdf(gen_name)==None and\
                    self.search_pdf(gen_name)==None:
                    self.log.error('can not find pdf file')
                    print(title)
                    has_error=True
        if has_error:
            self.log.error('number: %d',number)
        elif has_warning:
            self.log.warning('number: %d',number)

    def direct_pdf(self,gen_name): #exists: path+filename,not exists:None
        i=0
        for path in self.base_path:
            for root,dirs,files in os.walk(path):
                fullname=os.path.join(root,gen_name)
                try:
                    f=open(fullname,'r')
                    f.close()
                    return fullname
                except:
                    pass
        return None

    def search_pdf(self,gen_name): #exists: path+filename,not exists:None
        i=0
        for path in self.base_path:
            for root,dirs,files in os.walk(path):
                for filename in files:
                    if self.match(gen_name,filename):
                        return os.path.join(root,filename)
        return None

    def match(self, gen_name, filename):
        wfilename=wash_str(filename)
        sm=SequenceMatcher(None,gen_name,wfilename)
        if sm.real_quick_ratio()>0.9:
            if sm.quick_ratio()>0.9:
                #print(gen_name)
                #print(wfilename)
                #print(sm.real_quick_ratio())
                return True
        return False

    def void_row(self,row):
        for cell in row:
            if cell.value!=None:
                return False
        return True
    
if __name__=='__main__':
    filename='part_38.xlsx'
    chk=Checker(filename)#'pdf_buffer/')
    print('done')

