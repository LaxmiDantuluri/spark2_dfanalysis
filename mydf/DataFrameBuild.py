import re
import random
import string

import numpy as np
import pandas as pd

import pyspark as spark
from pyspark.sql.types import *
from pyspark.sql import functions as sf

# ---------------------------------------------------------
# df_array(x):

# ---------------------------------------------------------

class myDF():
    """
    :param simple_array:
    :param randomly_increasing_array:
    :param profile_size:
    :param profile_partitions:
    """
    def __init__(self,spark):
        # super(myDF, self).__init__()
        # self.arg = arg
        # self.df =
        self.spark = spark

    # def print_df(self):
        # self.count = self.df.count()

    def profile_size(self):
        pass


    def profile_partitions(self):
        pass

    def get_StructField(self,ctype):

        if re.search('str',ctype):
            field = StructField(ctype,StringType(),True)

        if re.search('int',ctype):
            field = StructField(ctype,IntegerType(),True)

        if re.search('double',ctype):
            field = StructField(ctype,DoubleType(),True)

        return field

    def get_string_array(self,w=8):
        '''
        Get an array of strings.
        :param w: the width of the string generated.
        '''
        # print("need a string of %d characters" % w)
        str1 = ''.join(random.choices(string.ascii_lowercase,k=w))
        return str1

    def get_integer_array(self,w=4,low=1000,high=9999):
        '''
        Get an array of strings.
        '''
        # print("need %d integers" % w)
        num = random.randint(low,high)
        return num


    def get_double_array(self,x=0.0,y=1.0):
        '''
        Get an array of strings.
        '''
        # print("need %d doubles" % n)
        num = random.random()
        return num


    def df_simple_array(self,*args):
        '''
        Create a simple, linear array.
        '''
        if len(args) == 0:
            n = 10
            s = 0
            total = n + 1
            self.df = self.spark.range(n).toDF("Index")

        elif len(args) == 1:
            if args[0] < 1:
                sys.exit(1)
            n = args[0]
            s = 0
            total = n + 1
            self.df = self.spark.range(n).toDF("Index")
        else:
            n = args[1]
            s = args[0]
            total = n - s + 1
            x = np.linspace(s,n,total)
            pdx = pd.DataFrame(x,columns=["Index"])
            self.df = self.spark.createDataFrame(pdx)

        self.count = total
        return self.df

    def df_randomly_increasing_array(self,n):
        """
        Randomly increasing variance.
        Build a 2D DataFrame from numpy arrays.
        arr1: linspaced
        arr2: random (increasing from between 1 and current row)
        """
        # print("Hello!!!!-2")
        domain = np.linspace(0,n-1,n)
        # print(domain)

        num_random = [np.random.randint(0,x+1) for x in domain]
        # print(num_random)

        # 2 tall columns
        data = np.vstack([domain,num_random]).transpose()

        # print(data.shape)

        # to pandas
        pdx = pd.DataFrame(data,columns=["Index","Random Number"])

        # to spark
        dfx = self.spark.createDataFrame(pdx)

        self.df = dfx
        return self.df

    def df_string_array(self,lst,label='value'):
        '''
        :param lst: a list of strings
        '''
        dfx = self.spark.createDataFrame(lst,StringType()).toDF(label)
        self.df = dfx
        return self.df


    def decision_array_type(self,ctype,n):
        '''
        Get an array as strings, integers, or doubles.
        '''
        # print("Getting a single array of type:",ctype," with %d rows." % n)

        if re.search('str',ctype):
            arr = self.get_string_array(n)
            return arr

        if re.search('int',ctype):
            arr = self.get_integer_array(n)
            return arr

        if re.search('double',ctype):
            arr = self.get_double_array(n)
            return arr


    def df_multidimensional(self,r,c,column_types,*kwargs):
        '''
        :param r:
        :param c:
        :param column_types:
        '''
        # print("Building a multidimensional array.")
        # print(r,c)
        # print(column_types)

        lst_total = []
        lst_fields = []

        for ctype in column_types:
            # print(ctype)
            field = self.get_StructField(ctype)

            lst_arr = []

            for i in range(r):
                entry = self.decision_array_type(ctype,r)

                # print(entry)
                lst_arr.append(entry)

            # print(field)
            lst_fields.append(field)
            lst_total.append(lst_arr)


        # print(lst_fields)
        # print(lst_total)

        lst_zipped = list(zip(*lst_total))
        # print(lst_zipped)

        pdx = pd.DataFrame(lst_zipped,columns=column_types)
        self.df = self.spark.createDataFrame(pdx)
        return self.df

        # ?? can I skip pandas?
        dfx = self.spark.createDataFrame(lst_total,lst_fields).toDF(column_types)
        self.df = dfx
        return dfx
