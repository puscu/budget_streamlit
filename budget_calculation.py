import pandas as pd

class BudgetGenerator:

    """
    Budget Generator Function:

    Needs to get the selected values from the user and calculate the budget multiplying the percentage of increase
    only to the selected zones, stores and products.

    If stores is not empty, zone will be not taken into account because store is a subsegment of zone.

    """
    def budget_generator(self, _df, _selected_values, _num_initiatives):

        generated_df = self.organic_growth(_df.copy())
        generated_df["Year"] = 2023

        if _num_initiatives > 0:

            for initiative in range(_num_initiatives):
                zones = _selected_values[f"selected_zone{initiative+1}"]
                stores = _selected_values[f"selected_store{initiative+1}"]
                products = _selected_values[f"selected_product{initiative+1}"]
                percentage = _selected_values[f"selected_percentage{initiative+1}"]

                mask = (
                    (generated_df['Dim1'].isin(zones) if len(zones) > 0 else True) &
                    (generated_df['Dim2'].isin(stores) if len(stores) > 0 else True) &
                    (generated_df['Dim4'].isin(products) if len(products) > 0 else True)
                )
                try:
                    generated_df.loc[mask, "Sales_Qty"] *= (1 + (percentage / 100))
                    generated_df.loc[mask, "Sales_Qty"] = round(generated_df.loc[mask, "Sales_Qty"], 2)
                except:
                    continue

        return generated_df
    

    def organic_growth(self, _df):

        """
        This function get as an input a DataFrame with historical sales by the 4 dimensions and Year/Month and Product
        and needs to calculate the organic growth.

        Can be calculated average sales giving more weigth to the last years and get the final df. Or making prediction via ML

        The dimension of the final df needs to be len(df)/years.uniques() and refers to the current year organic growth.
        """

        # In this case to keep it simple I am going to take last year and increase by 5%.
        organic_sales = _df[_df['Year'] == 2022]

        return organic_sales
