import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from static_inputs import StaticInputs, InventedInput
from budget_calculation import BudgetGenerator
from streamlit_utils import StreamlitUtils

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
st_utils = StreamlitUtils()

st.title(f"Commercial Budget {input_utils.get_current_year()}")
st.subheader("Forecast and Strategic Initiatives")

# Getting inputs
sales_df = pd.read_excel("input.xlsx")

sales_df['Date'] = pd.to_datetime(sales_df[['Year', 'Month']].assign(day=1))
dim1_selectbox = input_utils.get_dim1(sales_df)
dim2_selectbox = input_utils.get_dim2(sales_df)
dim4_selectbox = input_utils.get_dim4(sales_df)

### SIDEBAR ####
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
                                                                           min_value=-100.0, max_value=100.0, step=0.01, value=0.0)

    if i < num_choices - 1:
        st.sidebar.markdown("---")


#################

# Calculating Budget
budget_generator = BudgetGenerator()
budget = budget_generator.budget_generator(sales_df, selected_values, num_choices)

# Join with the original sales_df
sales_df_with_budget = pd.concat([sales_df, budget], axis=0)

# Create 3 columns
col1, col2, col3 = st.columns(3)

zone_graph= col1.multiselect("Select the Area", options=dim1_selectbox)
store_graph= col2.multiselect("Select the Store", options=dim2_selectbox)
product_graph= col3.multiselect("Select the Product", options=dim4_selectbox)

# Preparing DataFrame for the graph
if len(zone_graph) != 0 and len(store_graph) != 0 and len(product_graph) != 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim1"].isin(zone_graph) & sales_df_with_budget["Dim2"].isin(store_graph) & sales_df_with_budget["Dim4"].isin(product_graph)]
elif len(zone_graph) != 0 and len(store_graph) == 0 and len(product_graph) == 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim1"].isin(zone_graph)]
elif len(zone_graph) != 0 and len(store_graph) != 0 and len(product_graph) == 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim1"].isin(zone_graph) & sales_df_with_budget["Dim2"].isin(store_graph)]
elif len(zone_graph) == 0 and len(store_graph) != 0 and len(product_graph) != 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim2"].isin(store_graph) & sales_df_with_budget["Dim4"].isin(product_graph)]
elif len(zone_graph) != 0 and len(store_graph) == 0 and len(product_graph) != 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim1"].isin(zone_graph) & sales_df_with_budget["Dim4"].isin(product_graph)]
elif len(zone_graph) == 0 and len(store_graph) == 0 and len(product_graph) != 0:
    input_df = sales_df_with_budget[sales_df_with_budget["Dim4"].isin(product_graph)]
else:
    input_df = sales_df_with_budget

st.markdown("---")

dimension = st.selectbox("Which dimension do you want to see?", options=['Zone', 'Store', 'Product'])
if dimension == 'Zone':
    selected_dimension = 'Dim1'
elif dimension == 'Product':
    selected_dimension = 'Dim4'
else:
    selected_dimension = 'Dim2'


area_chart_data = input_df[['Year', selected_dimension, 'Sales_Qty']].groupby(by=['Year', selected_dimension]).sum()
area_chart_data.sort_values(by="Year")
area_chart_data.reset_index(inplace=True)
area_chart_data["Year_Text"] = area_chart_data["Year"].astype(str)

# Create bar chart with labels
fig = px.bar(area_chart_data, x='Year_Text', y='Sales_Qty', color=selected_dimension, 
             text=area_chart_data['Sales_Qty'].apply(lambda x: f'{x:,}'))

# Set layout properties
fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Sales',
    barmode='stack',
    showlegend=True
)

# Display chart
st.plotly_chart(fig)

# Create a matrix to visualize the % variation of the budget

grouped = input_df.groupby(by=[selected_dimension, 'Year'])['Sales_Qty'].sum()
df_grouped = pd.DataFrame(grouped)

min_year = df_grouped.index.get_level_values(1).min()

df_sorted = df_grouped.sort_values(by=[selected_dimension, 'Year'], ascending=True)
df_sorted['Pct_Change'] = df_sorted['Sales_Qty'].pct_change()*100
df_sorted['Pct_Change'] = df_sorted['Pct_Change'].map('{:.2f}%'.format)
df_sorted.loc[(slice(None), min_year), 'Pct_Change'] = 'NaN'

# Pivot the dataframe and calculate percentage variation
pivot_df = df_sorted.pivot_table(values='Pct_Change', index='Year', columns=selected_dimension, aggfunc=sum)

col4, col5 = st.columns(2)

col4.write(pivot_df)


col5.write('Review all your strategies and percentage variations. If you agree with the results generate the budget. It will be generated a formatted Excel file.')
col5.markdown('---')
click_generate = col5.button('Generate Budget')

if click_generate:
    st.write('Budget Generated')