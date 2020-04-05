from unidecode import unidecode
from re import search, split

def mtch_nm(nm_a, nm_b):
    mtch = False
    if nm_a == nm_b:
        mtch = True
    elif unidecode(nm_a) == unidecode(nm_b):
        mtch = True
    else:    
        sn_a = split(' ', unidecode(nm_a))
        sn_b = split(' ', unidecode(nm_b))
        if search(sn_a[0][0:-1] + '.+' + sn_a[1], nm_b) and '.' not in sn_a[1]: 
            mtch = True
        elif search(sn_b[0][0:-1] + '.+' + sn_b[1], nm_a) and '.' not in \
          sn_b[1]: 
            mtch = True
        elif len(sn_a) == 3:
            if search(sn_a[0] + '.+' + sn_a[2], nm_b):
                mtch = True
        elif len(sn_b) == 3:
            if search(sn_b[0] + '.+' + sn_b[2], nm_a):
                mtch = True

    return mtch