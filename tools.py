
def wash_str(s): #将特殊字符去除
    table={ 'Æ':'A','Á':'A','Â':'A','Â':'A',
            'À':'A','Å':'A','Ã':'A','Ä':'A',
            'Ç':'C','Ð':'D','É':'E','Ê':'E',
            'È':'E','Ë':'E','Í':'I','Î':'I',
            'Ì':'I','Ï':'I','Ñ':'N','Ó':'O',
            'Ô':'Ò','Ø':'O','Õ':'O','Ö':'O',
            'Þ':'P','Ú':'U','Û':'U','Ù':'U',
            'Ü':'U','Ý':'Y','á':'a', 
            'â':'a','æ':'a','à':'a','å':'a',
            'ã':'ä','ç':'c','é':'e','ê':'e',
            'è':'e','ð':'e','ë':'e','í':'i',
            'î':'i','ì':'i','ï':'i','ñ':'n',
            'ó':'o','ô':'o','ò':'o','ø':'o',
            'õ':'o','ö':'o','ß':'b','þ':'p',
            'ú':'u','û':'u','ù':'u','ü':'u',
            'ý':'y','ÿ':'y' }
    return ''.join(table[letter] if letter in table.keys() else
            letter for letter in s)

def title2filename(title, extension):
    filename_front=title
    banned_list=[':','"','/','?','<','>',"*",'\\']
    if filename_front[-1]=='.' or filename_front[-1]=='?':
        filename_front=filename_front[:-1]
    for l in banned_list:
        filename_front=filename_front.replace(l,'_')
    if extension[0]!='.':
        extension='.'+extension
    return filename_front+extension

def title2key(title):
    rm_list=['.','?',',',':','-','/','——','、',
            '(',')','[',']']
    title=wash_str(title).lower()
    for punct in rm_list:
        title=title.replace(punct,' ')
    key=title.split()
    if len(key)==1 and(key[0].isdigit() or key[0].isalpha()):
        return None
    return ' '.join(key)

def is_void_row(row):
    for cell in row:
        if cell.value!=None:
            return False
    return True

if __name__ == '__main__':
    s='''这是中文
    this a English
    C 'est français.
    Das ist Deutsch.'''
    # print(wash_str(s))
    print(title2filename('A: "Study" on Checkpointing for Distributed Applications Using Blockchain-Based Data Storage.','pdf'))

    
