import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import matplotlib.ticker as ticker
import warnings

warnings.filterwarnings("ignore")

API_URL = os.getenv("API_URL")

st.sidebar.title("UK Real Estate Insights")
st.sidebar.markdown("""
The UK housing market is a dynamic and evolving sector, shaped by economic trends, government policies, and global events. Property transactions, prices, and demand are influenced by a complex interplay of financial stability, investor sentiment, and regulatory frameworks.
By analyzing historical data, patterns in market behavior can be uncovered. This dashboard provides a data-driven perspective on the evolution of UK real estate.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Explore Market Trends")
selected_option = st.sidebar.radio(
    "Select a Topic:", 
    ["High-Value Neighborhoods in the UK Real Estate Market", "Impact of Historical Events on UK Real Estate"]
)


if selected_option == "Impact of Historical Events on UK Real Estate":
    st.title("Impact of Historical Events on UK Real Estate")

    st.markdown("""
        Several macroeconomic and political events have shaped the UK property market.  
        This analysis examines how these significant events have affected property sales over time:  

        - **The 2007-2009 Financial Crisis**: A global economic downturn caused a sharp decline in property transactions.  
        - **Brexit Referendum (2016)**: Political uncertainty led to changes in investment dynamics.  
        - **COVID-19 Pandemic (2020-2021)**: Lockdowns and remote work had a profound impact on buyer preferences.  

        The graph below highlights these key periods and illustrates how the market responded.
    """)

    response = requests.get(f"{API_URL}/sales-per-month")
    if response.status_code == 200:
        number_of_sales_df = pd.DataFrame(response.json())
        number_of_sales_df["date"] = pd.to_datetime(number_of_sales_df["date"])


        st.subheader("Monthly Sales in UK Real Estate Market (1995-2023)")
        plt.figure(figsize=(18,10))
        plt.plot(number_of_sales_df["date"], number_of_sales_df["num_sales"], linestyle="-", color="red")

        plt.xlabel("Transaction Date", fontsize=15)
        plt.ylabel("Number of Sales", fontsize=15)
        plt.ylim(0, 200000)
        plt.grid(True, linewidth=0.5)
        plt.xticks(rotation=0)

        plt.axvspan(datetime.datetime(2007, 12, 1), datetime.datetime(2009, 6, 1), color='blue', alpha=0.25, label="Financial Crisis")
        plt.axvspan(datetime.datetime(2016, 1, 1), datetime.datetime(2016, 6, 1), color='orange', alpha=0.25, label="Brexit Pre-Referendum")
        plt.axvspan(datetime.datetime(2020, 3, 1), datetime.datetime(2021, 11, 1), color='green', alpha=0.25, label="COVID-19 Pandemic")
        
        plt.legend(loc="upper left", fontsize=15)
        st.pyplot(plt)


        st.caption("""
            The UK housing market has exhibited varying degrees of volatility in response to macroeconomic and political shocks. During the 2008 financial crisis, transaction volumes plummeted as liquidity constraints tightened, restricting mortgage accessibility. The subsequent contraction in housing demand precipitated a decline in asset valuations.
            Leading up to the Brexit referendum (January - June 2016), transactional activity surged as investors sought to preempt regulatory and economic uncertainty. Market participants accelerated property acquisitions to mitigate potential capital depreciation post-vote, reflecting heightened risk aversion in the pre-referendum period.
            Conversely, the Covid-19 crisis demonstrated a different trajectory. While 2020 initially recorded a downturn in property sales due to restrictive measures and financial uncertainty, the market rebounded at a faster pace compared to 2008. Accommodative monetary policies, low interest rates, and fiscal stimuli stimulated demand, contributing to asset price inflation across multiple residential segments. 
        """)
    else:
        st.error("Error fetching data.")



if selected_option == "High-Value Neighborhoods in the UK Real Estate Market":
    st.title("High-Value Neighborhoods in the UK Real Estate Market")

    st.markdown("""
        The UK housing market exhibits strong regional differentiation, with certain neighborhoods consistently commanding premium valuations due to demand, infrastructure, and historical significance.  
        High-value districts often feature superior amenities, prestigious educational institutions, and connectivity to financial hubs, making them attractive to affluent buyers and investors.  
        Over time, shifts in economic conditions, urban development, and policy changes influence the pricing hierarchy of these elite areas. This analysis provides a broad perspective on the most expensive neighborhoods, showcasing key regional valuation trends and their evolution over the years.
    """)

    years = [str(year) for year in range(1995, 2024)]
    selected_year = st.selectbox("Select Year", years)

    response = requests.get(f"{API_URL}/top-expensive-neighborhoods?date={selected_year}")

    if response.status_code == 200:
        expensive_towns_df = pd.DataFrame(response.json())
        expensive_towns_df["full_name"] = expensive_towns_df["town"] + " - " + expensive_towns_df["district"]

        st.subheader(f"Most Expensive Neighborhoods in {selected_year}")
        plt.figure(figsize=(18,11))
        ax = sns.barplot(
            x=expensive_towns_df["full_name"], 
            y=expensive_towns_df["price"],
            palette="pastel",
            edgecolor="black",
            linewidth=1 
        )

        plt.xlabel("") 
        plt.ylabel("Average Price (£)", fontsize=12)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

        for index, row in expensive_towns_df.iterrows():
            plt.text(
                index, row["price"], f"£{row['price']:,.0f}",
                ha="center", va="bottom", fontsize=10, fontweight="bold", color="black"  
            )

        st.pyplot(plt)

        st.caption(f"""
            The barplot provides a comparative overview of the ten UK neighborhoods with the highest average transaction price in {selected_year}, highlighting market concentration in premium real estate locations.
        """)

    else:
        st.error("Error fetching data.")