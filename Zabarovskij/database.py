import os
import csv

class mydatabase(object):
    '''A class used to represent a database

    Attributes
    ----------
    location : str
        path to csv file with database
    db : dict
        database

    Methods
    -------
    load(location)
        Loads database from given location if it exists else create empty database
    _load
        Loads database from csv file stored in given location
    readdatafromcsv(location)
        reads data from csv file
    dumpdb(savepath)
        Save database into csv file
    set(key,colnumber,value)
        Edits data in database's cell
    add(value)
        Adds new row in database
    delete(key)
        Deletes row in database
    search(colnumber,value)
        Find given value in given column
    create(colnumber,valuelist)
        Creates new database containing row with values
    '''

    def __init__(self , location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self , location):
        '''Loads database from given location if it exists else create empty database

        Parameters
        ----------
        :param location: path to csv file with database
        :return bool: True if everything well
        '''
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}
        return True


    def _load(self):
        '''Loads database from csv file stored in given location
        '''
        rownumber,colnumber,data = self.readdatafromcsv(self.location)
        d = dict.fromkeys([i for i in range(rownumber)])
        for key in d:
            d[key] = data[key]
        self.db = d


    def readdatafromcsv(self,location):
        '''reads data from csv file
        
        Parameters
        ----------
        :return rownumber: number of rows in database
        :return colnumber: number of columns in database
        :return data: data from database
        '''
        with open(location, newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        rownumber = len(data) # число строк
        colnumber = len(data[0]) # число столбцов
        return rownumber,colnumber,data


    def dumpdb(self,savepath):
        '''Save database into csv file

        Parameters
        ----------
        :param savepath: path to save csv file
        :return bool: True if everything well 
        '''
        savepath=os.path.expanduser(savepath)
        print('savepath',savepath,'self.db',self.db)
        try:
            with open(savepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                print('writer',writer)
                for key in self.db:
                    writer.writerow(self.db[key])
                    print('key',key,'self.db',self.db)
            return True
        except:
            return False


    def set(self,key,colnumber,value):
        '''Edits data in database's cell

        Parameters
        ----------
        :param key: unique cell's row number
        :param colnumber: cell's column number
        :param value: value in cell
        :reurn bool: True if everything well
        '''
        try:
            self.db[key][colnumber] = value
            # self.dumpdb(self.location)
            print(self.db)
            return True
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False


    def add(self,value):
        '''Adds new row in database

        Parameters
        ----------
        :param value: list of values with value for each column in new row
        :reurn bool: True if everything is well
        '''
        try:
            keys = self.db.keys()
            lastkey = sorted(keys)[-1]
            nextkey = lastkey + 1
            self.db[nextkey] = value
            print(self.db)
            return True
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False


    def delete(self,key):
        '''Deletes row in database

        Parameters
        ----------
        :param key: unique row number
        :return bool: True if everything is well
        '''
        if not key in self.db:
            return False
        del self.db[key]
        return True

    def search(self,colnumber,value):
        '''Find given value in given column

        Parameters
        ----------
        :param colnumber: column number
        :param value: value
        :return keylist: list of unique row numbers, containing given value
        '''
        keylist=[]
        for key in self.db:
            if self.db[key][colnumber] == value:
                keylist.append(key)
        return keylist


    def create(self,colnumber,valuelist):
        '''Creates new database containing row with values

        Parameters
        ----------
        :param valuelist: list of values for 1 row
        :return self.db: database
        '''
        self.db={}
        key=0
        self.db[key]=valuelist
        return self.db

