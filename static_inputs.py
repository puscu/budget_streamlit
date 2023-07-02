import pandas as pd
import datetime
import numpy as np
import random

class InventedInput:

    dim1 = ['Zone A', 'Zone B', 'Zone C']
    
    dim2 = {}
    dim3 = {}

    for zone in dim1:
        # Creating 3 random stores for every zone and 5 random vendors for every store
        stores = []
        
        for i in range(0, 3):
            store = zone + " - " + str(random.randint(1, 100))
            stores.append(store)
            vendors = []
            for z in range(0, 5):
                vendors.append(f"Vendor {store} - {str(random.randint(1, 100))}")
            dim3[store] = vendors
        dim2[zone] = stores

    dim4 = {'Mouse', 'Keyboard'}

    years = [2019, 2020, 2021, 2022]

    def get_dim1(self):
        return self.dim1
    
    def get_dim2(self):
        return self.dim2
    
    def get_dim3(self):
        return self.dim3
    
    def get_dim4(self):
        return self.dim4
    
    def generate_sales(self):

        zones = self.dim1
        stores = self.dim2
        vendors = self.dim3
        products = self.dim4
        years = self.years

        sales_dictionary = {
            'Dim1': None,
            'Dim2': None,
            'Dim3': None,
            'Dim4': None,
            'Year': None,
            'Month': None,
            'Sales_Qty': None
        }

        dim1_list = []
        dim2_list = []
        dim3_list = []
        dim4_list = []
        year_list = []
        month_list = []
        sales_list = []

        for year in years:
            for month in range(1, 13):
                for zone in zones:
                    stores_zone = stores[zone]
                    for store in stores_zone:
                        vendors_store = vendors[store]
                        for vendor in vendors_store:
                            for product in products:
                                dim1_list.append(zone)
                                dim2_list.append(store)
                                dim3_list.append(vendor)
                                dim4_list.append(product)
                                year_list.append(year)
                                month_list.append(month)
                                sales_list.append(random.randint(1, 10000))

        sales_dictionary['Dim1'] = dim1_list
        sales_dictionary['Dim2'] = dim2_list
        sales_dictionary['Dim3'] = dim3_list
        sales_dictionary['Dim4'] = dim4_list
        sales_dictionary['Year'] = year_list
        sales_dictionary['Month'] = month_list
        sales_dictionary['Sales_Qty'] = sales_list

        df_sales = pd.DataFrame(sales_dictionary)

        return df_sales


class StaticInputs:

    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    current_year = datetime.datetime.now().year

    def get_months_list(self):
        return self.months
    
    def get_current_year(self):
        return self.current_year
    
    def get_dim1(self, df):
        return df['Dim1'].unique().tolist()
    
    def get_dim2(self, df):
        return df['Dim2'].unique().tolist()
    
    def get_dim3(self, df):
        return df['Dim3'].unique().tolist()
    
    def get_dim4(self, df):
        return df['Dim4'].unique().tolist()