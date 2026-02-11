import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from components import Chart

st.set_page_config(
    page_title="Sales Analysis | Acme",
    layout="wide"
)

st.header("📊 Sales Analysis")
st.caption("Acme Corporation — performance, trends, and revenue insights")

c = Chart('data/sales_data.csv')
with st.sidebar:
    year = st.selectbox('Year:', options=c.year())
    month = st.selectbox('Month:', options=c.month())
    us_region = st.selectbox('Region: ', options=c.us_region())
    channel = st.selectbox('Channel: ', options=c.channel())

    year = None if year == "All" else year
    month = None if month == "All" else month
    region = None if us_region == "All" else us_region
    channel = None if channel == "All" else channel


total_revenue, total_profit, profit_margin, total_orders, revenue_per_order = c.compute_kpis(
    year, month, region, channel)

cols = st.columns(5, gap="small")

with cols[0]:
    st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
with cols[1]:
    st.metric("📈 Total Profit", f"${total_profit:,.0f}")
with cols[2]:
    st.metric("📊 Profit Margin", f"{profit_margin:,.1f}%")
with cols[3]:
    st.metric("🛒 Total Orders", f"{total_orders:,}")
with cols[4]:
    st.metric("🤑 Rev / Order", f"${revenue_per_order:,.0f}")


style_metric_cards(
    background_color="transparent",
    border_size_px=0,
    border_radius_px=12,
    border_left_color="#6366f1",
    box_shadow=True
)

st.plotly_chart(c.us_map_reveue(year, month, region, channel), width='stretch',
                config={'displayModeBar': False})

tab1, tab2, tab3 = st.tabs([
    "📊 Executive Overview & Trends",
    "📦 Product & Channel Performance",
    "🌎 Geographic & Customer Insights"
])

with tab1:
    st.header("Executive Overview & Trends")

    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.monthy_revenue_rhythm(
            year, month, region, channel), width='stretch')

    with colA2:
        st.plotly_chart(c.profit_pulse(
            year, month, region, channel), width='stretch')

    colB1, colB2 = st.columns(2)

    with colB1:
        st.plotly_chart(c.order_value_spectrum(
            year, month, region, channel), width='stretch')

    with colB2:
        st.plotly_chart(c.high_margin_price_bands(
            year, month, region, channel), width='stretch')


with tab2:
    st.header("Product & Channel Performance")

    colA1, colA2, colA3 = st.columns(3)
    with colA1:
        st.plotly_chart(c.revenue_chamption(
            year, month, region, channel), width='stretch')

    with colA2:
        st.plotly_chart(c.high_margin_heros(
            year, month, region, channel), width='stretch')

    with colA3:
        st.plotly_chart(c.stratetic_profit(
            year, month, region, channel), width='stretch')

    colB1, colB2, colB3 = st.columns(3)
    channel_df = c.channel_df(year, month, region, channel)

    with colB1:
        st.plotly_chart(c.channel_chart(
            channel_df, "Channel Revenue Play: Where the Revenue Come", "total_revenue"), width='stretch')

    with colB2:
        st.plotly_chart(c.channel_chart(
            channel_df, "Profit Pipeline by Channel Who's Really Paying", "total_profit"), width='stretch')

    with colB3:
        st.plotly_chart(c.channel_chart(
            channel_df, "Channel Efficiency Score: Margin per sale by route", "margin_per_sale"), width='stretch')

with tab3:
    st.header("Geographic & Customer Insights")

    top_tab, bottom_tab = st.tabs(['Top 5', "Bottom 5"], width='stretch')

    with top_tab:
        colA1, colA2, colA3 = st.columns(3)
        with colA1:
            st.plotly_chart(c.top_customer_revenue(
                year, month, region, channel), width='stretch')

        with colA2:
            st.plotly_chart(c.top_customer_profit_margin(
                year, month, region, channel), width='stretch')

        with colA3:
            st.plotly_chart(c.top_state_revenue(
                year, month, region, channel), width='stretch')

    with bottom_tab:
        colB1, colB2, colB3 = st.columns(3)
        with colB1:
            st.plotly_chart(c.bottom_customer_revenue(
                year, month, region, channel), width='stretch')

        with colB2:
            st.plotly_chart(c.bottom_customer_profit_margin(
                year, month, region, channel), width='stretch')

        with colB3:
            st.plotly_chart(c.bottom_state_revenue(
                year, month, region, channel), width='stretch')

    colC1, colC2 = st.columns(2)

    with colC1:
        st.plotly_chart(c.revenue_region(
            year, month, region, channel), width='stretch')

    with colC2:
        st.plotly_chart(c.profit_region(
            year, month, region, channel), width='stretch')
