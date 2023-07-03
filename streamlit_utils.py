import altair as alt

class StreamlitUtils:

    def get_chart(self, data):
        
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
                y=alt.Y("sum(Sales_Qty)", title="Sales Quantity"),
                color="Dim1",
            )
        )

        # Draw points on the line, and highlight based on selection
        points = lines.transform_filter(hover).mark_circle(size=65)

        labels = (
            lines.mark_text(align='center', baseline='middle', dy=-5, fontSize=10)
            .encode(
                x="Year_Text",
                y="Sales_Qty",
                text="Sales_Qty:Q",
                detail="Dim1",
            )
        )

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
                    alt.Tooltip("Dim1", title="Zone"),
                    alt.Tooltip("Sales_Qty", title="Sales Quantity"),
                ],
            )
            .add_selection(hover)
        )
        return (lines + labels + tooltips).interactive()