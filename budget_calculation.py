import pandas as pd

class BudgetGenerator:

    """
    Budget Generator Function:

    Needs to get the selected values from the user and calculate the budget multiplying the percentage of increase
    only to the selected zones, stores and products.

    If stores is not empty, zone will be not taken into account because store is a subsegment of zone.

    """
    def budget_generator(self, _df, _selected_values, _num_initiatives):

        generated_df = pd.DataFrame()

        if _num_initiatives == 0:
            generated_df = _df

        for initiative in range(_num_initiatives):
            zones = _selected_values[f"selected_zone{initiative+1}"]
            stores = _selected_values[f"selected_store{initiative+1}"]
            products = _selected_values[f"selected_product{initiative+1}"]
            percentage = _selected_values[f"selected_percentage{initiative+1}"]

            if len(stores) != 0:
                if len(products) != 0:
                    generated_df = _df[(_df['Dim2'].isin(stores)) & (_df['Dim4'].isin(products))]
                else:
                    generated_df = _df[(_df['Dim2'].isin(stores))]
            elif len(zones) != 0:
                if len(products) != 0:
                    generated_df = _df[(_df['Dim1'].isin(stores)) & (_df['Dim4'].isin(products))]
                else:
                    generated_df = _df[(_df['Dim1'].isin(stores))]
            elif len(products) != 0:
                generated_df = _df[(_df['Dim4'].isin(stores))]
            else:
                generated_df = _df

            generated_df["Year"] = 2023
            generated_df["Sales_Qty"] = generated_df["Sales_Qty"]*(1 + (percentage/100))

        return generated_df