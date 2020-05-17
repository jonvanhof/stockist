import sqlite3


class Object:
    def __init__(self, name, fields, shelf_life, db_conn):
        self.nm = name

        if type(fields) != dict:
            raise ValueError('Invalid definition of fields: input must '
                             'be dictionary.')
        else:
            for i, j in fields.items():
                if j[-2:] == 'pk':
                    ft = j[:-3]
                else:
                    ft = j
                if ft not in ('string', 'int', 'float', 'bool', 'datetime'):
                    raise ValueError('Invalid data type included in fields')
        self.fields = fields

        if type(shelf_life) != int:
            raise ValueError('Shelf life must be a integer number of days.')
        self.shelf_life = shelf_life

        self.conn = db_conn
        self.curs = self.conn.cursor()
        self.create_tbl()

    def create_tbl(self):
        try:
            self.curs.execute('select * from ' + self.nm + ';')
        except sqlite3.OperationalError:
            tbl_string = "("
            for i, j in self.fields.items():
                is_pk = False
                if j[-2:] == 'pk':
                    is_pk = True
                    ft = j[:-3]
                else:
                    ft = j
                if ft == 'string' or ft == 'datetime':
                    tbl_string += i + " text"
                elif ft == 'int' or ft == 'boolean':
                    tbl_string += i + " integer"
                elif ft == 'float':
                    tbl_string += i + " real"

                if is_pk:
                    tbl_string += " primary key"
                if i != list(self.fields)[-1]:
                    tbl_string += ", "
                else:
                    tbl_string += "upd_dt text"
                    tbl_string += ")"

            self.curs.execute('create table ' + self.nm + ' ' + tbl_string)

    def get(self, params=None):
        if not params:
            self.curs.execute('select * from ' + self.nm + ';')
        else:
            where_string = ""
            for i, j in params.items():
                where_string += i + " = " + j + ", "
            where_string = where_string[:-2]
            self.curs.execute('select * from ' + self.nm + ' where ' +
                              where_string + ';')
        res_list = self.curs.fetchall()

        ret_list = []
        for i in res_list:
            ret_row = {}
            for j in range(len(i)):
                ret_row[list(self.fields)[j]] = i[j]
            ret_list.append(ret_row)

        return ret_list

    def put(self, values):
        pk = ""
        field_string = "("
        for i, j in self.fields.items():
            if j[-2:] == 'pk':
                pk = i
            field_string += i + ", "
        field_string = field_string[:-2] + ")"

        for i in values:
            val_string = ""
            set_string = ""
            for j, k in i.items():
                val_string += '"' + k + '"' + ", "
                if pk != j:
                    set_string += j + "=excluded." + j + ", "
            val_string = val_string[:-2]
            set_string = set_string[:-2]

            if pk == "":
                self.curs.execute('insert into ' + self.nm + ' ' +
                                  field_string + '  values ' + '(' +
                                  val_string + ')')
            else:
                self.curs.execute('insert into ' + self.nm + ' ' +
                                  field_string + '  values ' + '(' +
                                  val_string + ') on conflict(' + pk +
                                  ') do update set ' + set_string + ';')

        self.conn.commit()
