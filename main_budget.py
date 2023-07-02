import pandas as pd
import streamlit as st
import altair as alt

from static_inputs import StaticInputs, InventedInput

### Main Page of the Budget App ###

#The App enables the decisions makers of a company to automatically generate a commercial budget for the next year.
#In companies, what usually happens is that the budget definition is a long process. There are a lot of manual steps performed,
#lots of people involved and there is no methodology to do it.

#With this tool, it will be possible to have a annual forecast of sales taking historical data as input and it will be possible
#to adjust the budget with strategical or specific initiatives.

#Input of the DB for the forecast:
#-Dim 1 --> Could be area
#-Dim 2 --> Could be store/office
#-Dim 3 --> Could be vendor
#-Dim 4 --> Could be product
#-Year --> Sales Year
#-Month --> Sales Month
#-Sales Qty --> Sales Quantity

#Input for the Adjustments:
#-Dropdown Select Box for all the dimensions --> Dim1, Dim2, Dim3, Dim4
#-Slider to select a specific % impact on sales
#-Dropdown Select Box to define the period of time affected by the initiative
###

input_utils = StaticInputs()
invented_inputs = InventedInput()

st.title(f"Commercial Budget {input_utils.get_current_year()}")
st.subheader("Forecast and Strategic Initiatives")

# Getting inputs
sales_df = invented_inputs.generate_sales()
sales_df['Date'] = pd.to_datetime(sales_df[['Year', 'Month']].assign(day=1))
dim1_selectbox = input_utils.get_dim1(sales_df)
dim2_selectbox = input_utils.get_dim2(sales_df)
dim4_selectbox = input_utils.get_dim4(sales_df)

# Preparing Sidebar for the Parameters of the Strategic and Commercial Initiatives
st.sidebar.subheader("Parameters of the Strategic and Commercial Initiatives")
num_choices = st.sidebar.slider("Select the number of Strategic and Commercial Initiatives you want to add to the budget this year", 
                  min_value=0, 
                  max_value=5)

selected_values = {}

for i in range(num_choices):

    selected_values[f"selected_zone{i+1}"] = st.sidebar.multiselect(f"Select the Area {i+1}", options=dim1_selectbox)
    selected_values[f"selected_store{i+1}"] = st.sidebar.multiselect(f"Select the Store {i+1}", options=dim2_selectbox)
    selected_values[f"selected_product{i+1}"] = st.sidebar.multiselect(f"Select the Product {i+1}", options=dim4_selectbox)
    selected_values[f"selected_percentage{i+1}"] = st.sidebar.number_input(f"Choose the percentage of increase (in %) for initiative {i+1}", 
                                                                           min_value=0.0, max_value=100.0, step=0.01)

    if i < num_choices - 1:
        st.sidebar.markdown("---")

# Create two columns
col1, col2, col3 = st.columns(3)

zone_graph= col1.multiselect("Select the Area", options=dim1_selectbox)
store_graph= col2.multiselect("Select the Store", options=dim2_selectbox)
product_graph= col3.multiselect("Select the Product", options=dim4_selectbox)

# Preparing DataFrame for the graph
if len(zone_graph) != 0 and len(store_graph) != 0 and len(product_graph) != 0:
    input_df = sales_df[sales_df["Dim1"].isin(zone_graph) & sales_df["Dim2"].isin(store_graph) & sales_df["Dim4"].isin(product_graph)]
elif len(zone_graph) != 0 and len(store_graph) == 0 and len(product_graph) == 0:
    input_df = sales_df[sales_df["Dim1"].isin(zone_graph)]
elif len(zone_graph) != 0 and len(store_graph) != 0 and len(product_graph) == 0:
    input_df = sales_df[sales_df["Dim1"].isin(zone_graph) & sales_df["Dim2"].isin(store_graph)]
elif len(zone_graph) == 0 and len(store_graph) != 0 and len(product_graph) != 0:
    input_df = sales_df[sales_df["Dim2"].isin(store_graph) & sales_df["Dim4"].isin(product_graph)]
elif len(zone_graph) != 0 and len(store_graph) == 0 and len(product_graph) != 0:
    input_df = sales_df[sales_df["Dim1"].isin(zone_graph) & sales_df["Dim4"].isin(product_graph)]
else:
    input_df = sales_df

area_chart_data = input_df[['Year', 'Dim1', 'Sales_Qty']].groupby(by=['Year', 'Dim1']).sum()
area_chart_data.sort_values(by="Year")
area_chart_data.reset_index(inplace=True)
area_chart_data["Year_Text"] = area_chart_data["Year"].astype(str)

# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_single(
        fields=["Year"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    #.mark_line()
    lines = (
        alt.Chart(data, title="Evolution of Sales").mark_bar()
        .encode(
            x="Year_Text",
            y="Sales_Qty",
            color="Dim1",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            #x="yearmonthdate(Date)",
            x='Year_Text',
            y="Sales_Qty",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Year_Text", title="Year"),
                alt.Tooltip("Sales_Qty", title="Sales Quantity"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

chart = get_chart(area_chart_data)

st.altair_chart(chart.interactive(), use_container_width=True)