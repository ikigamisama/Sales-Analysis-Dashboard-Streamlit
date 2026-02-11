import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


class Chart:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.data_preprocessing()

    def data_preprocessing(self):
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])

    def filter_data(self, year=None, month=None, us_region=None, channel=None):
        df = self.df.copy()

        if year is not None:
            df = df[df["order_date"].dt.year == year]

        if month is not None:
            df = df[df["order_month_name"] == month]

        if us_region is not None:
            df = df[df["us_region"] == us_region]

        if channel is not None:
            df = df[df["channel"] == channel]

        return df

    def year(self):
        return ['All'] + self.df['order_date'].dt.year.unique().tolist()

    def month(self):
        return ['All'] + self.df['order_month_name'].unique().tolist()

    def us_region(self):
        return ['All'] + self.df['us_region'].unique().tolist()

    def channel(self):
        return ['All'] + self.df['channel'].unique().tolist()

    def compute_kpis(self, year=None, month=None, us_region=None, channel=None):
        df = self.filter_data(year, month, us_region, channel)
        total_revenue = df['revenue'].sum().item()
        total_profit = df['profit'].sum().item()
        profit_margin = df['profit'].sum().item() / \
            df['revenue'].sum().item() * 100
        total_orders = df['order_number'].count().item()
        revenue_per_order = df['revenue'].sum().item() / \
            df['order_number'].count().item()

        return total_revenue, total_profit, profit_margin, total_orders, revenue_per_order

    def monthy_revenue_rhythm(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel)
        df = df.groupby(['order_month_name', 'order_month_num'])[
            'revenue'].sum().reset_index().sort_values('order_month_num')

        fig = px.line(df, x='order_month_name', y='revenue',
                      markers=True, line_shape='spline')

        fig.update_traces(
            line=dict(color='#7161EF'),
            marker=dict(color='#7161EF')
        )
        fig.update_layout(
            title='Monthly Revenue Rhythm: Uncovering Seasonality Peaks',
            xaxis_title=None,
            yaxis_title=None,
            height=300,
        )
        return fig

    def profit_pulse(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel)
        df = df.groupby(['order_month_name', 'order_month_num'])['profit'].sum().round(
            2).reset_index().sort_values('order_month_num', ascending=True)

        fig = px.line(df, x='order_month_name',
                      y='profit', markers=True, line_shape='spline')

        fig.update_traces(
            line=dict(color='#7161EF'),
            marker=dict(color='#7161EF')
        )
        fig.update_layout(
            title='Profit Pulse: Tracking Monthly Earnings Momentum',
            xaxis_title=None,
            yaxis_title=None,
            height=300,
        )
        return fig

    def order_value_spectrum(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby(
            'order_number')['revenue'].sum().reset_index()

        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=df["revenue"],
                nbinsx=50,
                name="Order Value",
                marker=dict(
                    color="#7161ef",
                    line=dict(width=0)
                ),
                opacity=0.85
            )
        )

        fig.update_layout(
            title="Order Value Spectrum: Mapping Customer Spending Tiers",
            xaxis_title=None,
            yaxis_title=None,
            bargap=0.2,
            template="plotly_white"
        )

        return fig

    def high_margin_price_bands(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel)
        fig = go.Figure()

        fig.add_trace(go.Scattergl(
            x=df["unit_price"],
            y=df["profit_margin_pct"],
            mode="markers",
            marker=dict(
                size=5,
                color="#7161EF",
                opacity=0.6,
                line=dict(width=0)
            ),
            text=df["product_name"],
            customdata=df.index,
            hovertemplate=(
                "Product: %{text}<br>" +
                "Unit Price: $%{x:.2f}<br>" +
                "Margin %: %{y:.2f}<br>" +
                "<extra></extra>"
            )
        ))

        # --- Layout customization ---
        fig.update_layout(
            title=f"Product Positioning: Price vs Margin (Revenue Weighted)",
            xaxis_title="Unit Price ($)",
            yaxis_title="Profit Margin (%)",
            dragmode="lasso",
            height=500,
            margin=dict(l=40, r=40, t=60, b=40)
        )

        return fig

    def revenue_chamption(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('product_name')[
            'revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["revenue"],
            y=df["product_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["revenue"],
            textposition="inside",
            texttemplate="$%{text:,.2f}"
        ))

        fig.update_layout(
            title="Revenue Champions: Best Selling Products Driving Growth",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    def high_margin_heros(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('product_name').agg(
            revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
        df['profit_margin_pct'] = (df['profit'] / df['revenue'] * 100).round(2)
        df = df.sort_values('profit_margin_pct', ascending=False).head(10)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["profit_margin_pct"],
            y=df["product_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["profit_margin_pct"],
            textposition="inside",
            texttemplate="%{text:,.1f}%"
        ))

        fig.update_layout(
            title="High-Margin Heroes: Most Efficient Products to Sell",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    def stratetic_profit(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('customer_name').agg(total_revenue=('revenue', 'sum'), total_profit=(
            'profit', 'sum'), average_profit_margin=('profit_margin_pct', 'mean'), order_count=('order_number', 'nunique')).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["total_revenue"],
            y=df["average_profit_margin"],
            mode="markers",
            marker=dict(
                size=8,
                color="#7161EF",
                opacity=0.7
            ),
            text=df.index,  # hover label
            customdata=df.index,  # row index hook
            hovertemplate="Revenue: %{x}<br>" +
            "Margin %: %{y}<br>" +
            "<extra></extra>"
        ))
        fig.update_layout(
            title="Strategic Product Position: Revenue vs Profit Margin",
            xaxis_title="Revenue",
            yaxis_title="Average Profit Margin %",
            height=500,
            dragmode="lasso"
        )
        return fig

    def channel_df(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('channel').agg(total_revenue=('revenue', 'sum'), total_profit=(
            'profit', 'sum'), margin_per_sale=('profit_margin_pct', 'mean')).reset_index()

        df['total_revenue'] = df['total_revenue'].round(2)
        df['total_profit'] = df['total_profit'].round(2)
        df['margin_per_sale'] = df['margin_per_sale'].round(2)

        return df

    def channel_chart(self, df, title, values):
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=df["channel"],
            values=df[values],
            hole=0.7,
            marker_colors=["#f5f5f5", "#12239e", "#7161EF"],
            texttemplate="$%{value:,.2f}<br>(%{percent})",
            textposition="outside"
        ))
        fig.update_layout(
            title=title,
            xaxis_title=None,
            yaxis_title=None,
            height=450,
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.20,
                yanchor="top"
            ),
            margin=dict(
                t=150
            )
        )
        return fig

    def top_customer_revenue(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('customer_name')[
            'revenue'].sum().round(2).reset_index().sort_values('revenue', ascending=False).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["revenue"],
            y=df["customer_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["revenue"],
            textposition="inside",
            texttemplate="$%{text:,.2f}"
        ))

        fig.update_layout(
            title="Top 5 Customers by Revenue",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    def top_customer_profit_margin(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('customer_name').agg(
            total_revenue=('revenue', 'sum'), total_profit=('profit', 'sum')).reset_index()
        df['profit_margin_pct'] = (
            df['total_profit'] / df['total_revenue'] * 100).round(2)
        df = df.sort_values('profit_margin_pct', ascending=False).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["profit_margin_pct"],
            y=df["customer_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["profit_margin_pct"],
            textposition="inside",
            texttemplate="%{text:,.2f}%"
        ))

        fig.update_layout(
            title="Top 5 Customers by Profit Margin",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    def top_state_revenue(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('state_name')[
            'revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["revenue"],
            y=df["state_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["revenue"],
            textposition="inside",
            texttemplate="$%{text:,.2f}"
        ))

        fig.update_layout(
            title="Top 5 State by Revenue",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    def bottom_customer_revenue(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('customer_name')[
            'revenue'].sum().reset_index().sort_values('revenue', ascending=True).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["revenue"],
            y=df["customer_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["revenue"],
            textposition="inside",
            texttemplate="$%{text:,.2f}"
        ))

        fig.update_layout(
            title="Bottom 5 Customers by Revenue",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        return fig

    def bottom_customer_profit_margin(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('customer_name').agg(
            total_revenue=('revenue', 'sum'), total_profit=('profit', 'sum')).reset_index()

        df['profit_margin_pct'] = (
            df['total_profit'] / df['total_revenue'] * 100).round(2)
        df = df.sort_values('profit_margin_pct', ascending=True).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["profit_margin_pct"],
            y=df["customer_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["profit_margin_pct"],
            textposition="inside",
            texttemplate="%{text:,.2f}%"
        ))

        fig.update_layout(
            title="Bottom 5 Customers by Margin",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        return fig

    def bottom_state_revenue(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('state_name')[
            'revenue'].sum().reset_index().sort_values('revenue', ascending=True).head(5)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["revenue"],
            y=df["state_name"],
            orientation="h",
            marker_color="#7161EF",
            text=df["revenue"],
            textposition="inside",
            texttemplate="$%{text:,.2f}"
        ))

        fig.update_layout(
            title="Bottom 5 State by Revenue",
            xaxis_title=None,
            yaxis_title=None,
            height=500
        )
        return fig

    def revenue_region(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('us_region')[
            'revenue'].sum().reset_index().sort_values('us_region', ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=df["us_region"],
            values=df["revenue"],
            hole=0.7,
            marker_colors=["#ccff33", "#12239e", "#f5f5f5", '#7161EF'],
            texttemplate="$%{value:,.2f}<br>(%{percent})",
            textposition="outside",
            sort=False
        ))
        fig.update_layout(
            title="Total Revenue by Region",
            xaxis_title=None,
            yaxis_title=None,
            height=450,
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.25,
                yanchor="top"
            ),
            margin=dict(
                t=150
            )
        )
        return fig

    def profit_region(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby('us_region')[
            'profit_margin_pct'].mean().reset_index().sort_values('us_region', ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=df["us_region"],
            values=df["profit_margin_pct"],
            hole=0.7,
            marker_colors=["#ccff33", "#12239e", "#f5f5f5", '#7161EF'],
            texttemplate="%{value:,.2f}%<br>(%{percent})",
            textposition="outside",
            sort=False
        ))
        fig.update_layout(
            title="Profit Margin by Region",
            xaxis_title=None,
            yaxis_title=None,
            height=450,
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.25,
                yanchor="top"
            ),
            margin=dict(
                t=150
            )
        )
        return fig

    def us_map_reveue(self, year, month, us_region, channel):
        df = self.filter_data(year, month, us_region, channel).groupby(
            'state')['revenue'].sum().reset_index()
        fig = px.choropleth(
            df,
            locations="state",
            locationmode="USA-states",
            color="revenue",
            scope="usa",
            color_continuous_scale="Inferno",
            range_color=(df["revenue"].min() * 0.9,
                         df["revenue"].max() * 1.1),
            labels={"revenue": "Revenue ($)"},
            title="Revenue by US State",
            template="plotly_dark" if st.get_option(
                "theme.base") == "dark" else "plotly",
        )

        fig.update_layout(
            title_font_size=22,
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
                showland=True,
                landcolor="lightgray" if st.get_option(
                    "theme.base") != "dark" else "#2d3748",
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(l=0, r=0, t=60, b=0),
            height=500,
            coloraxis_colorbar=dict(
                title="Revenue",
                thickness=15,
                len=0.7,
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1.02,
            ),
        )

        return fig
