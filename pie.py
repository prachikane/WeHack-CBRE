import pandas as pd
import matplotlib.pyplot as plt
def setPie(st):
    # Sample data with sector names and performance metrics
    data = {
        'Sector': ['Tech', 'Finance', 'Healthcare', 'Consumer', 'Energy'],
        'Performance': [25, 20, 15, 12, 10]  # You should replace these values with actual performance data
    }

    # Create a Pandas DataFrame from the data
    df = pd.DataFrame(data)

    # Sort the DataFrame by performance in descending order and select the top 5 sectors
    top_5_sectors = df.sort_values(by='Performance', ascending=False).head(5)

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(top_5_sectors['Performance'], labels=top_5_sectors['Sector'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    # Display the pie chart in Streamlit
    st.subheader("Top 5 Performing Sectors")
    st.pyplot(fig)

    # Display the table of top 5 sectors
    st.dataframe(top_5_sectors)
