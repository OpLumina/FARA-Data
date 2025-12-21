import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dataset
# Uses 'latin1' to handle special characters and 'on_bad_lines' to skip corrupted rows
df = pd.read_csv('FARA_All_ForeignPrincipals.csv', on_bad_lines='skip', encoding='latin1')

# 2. Data Cleaning & Status Calculation
# Determine if a principal is Active or Terminated
df['Status'] = df['Foreign Principal Termination Date'].apply(
    lambda x: 'Terminated' if pd.notnull(x) else 'Active'
)

# Convert dates to datetime for temporal analysis
df['Registration Date'] = pd.to_datetime(df['Foreign Principal Registration Date'], errors='coerce')
df['Year'] = df['Registration Date'].dt.year

# 3. Aggregate Analytics by Country (Column D)
country_stats = df.groupby('Country/Location Represented').agg(
    Total_Registrations=('Foreign Principal', 'count'),
    Active_Registrations=('Status', lambda x: (x == 'Active').sum()),
    Terminated_Registrations=('Status', lambda x: (x == 'Terminated').sum()),
    Unique_Registrants=('Registrant Name', 'nunique')
).reset_index()

# Sort by the most registrations and save the full list to CSV
country_stats = country_stats.sort_values(by='Total_Registrations', ascending=False)
country_stats.to_csv('all_countries_fara_analytics.csv', index=False)

# 4. GRAPHING: All Countries Bar Chart
# We use a horizontal chart with a height of 45 inches to fit all labels
plt.figure(figsize=(12, 45))
plt.barh(country_stats['Country/Location Represented'], country_stats['Total_Registrations'], color='skyblue', edgecolor='navy')
plt.title('FARA Registrations: All Countries/Locations')
plt.xlabel('Number of Registrations')
plt.ylabel('Country/Location')
plt.gca().invert_yaxis() # Put the highest counts at the top
plt.tight_layout()
plt.savefig('all_countries_registrations.png')

# 5. GRAPHING: Temporal Trend for All Countries
# Group by Year and Country
df_trend = df.groupby(['Year', 'Country/Location Represented']).size().unstack().fillna(0)

plt.figure(figsize=(15, 8))
# Plotting all columns. Legend is disabled because 266 items would block the view.
df_trend.rolling(window=3).mean().plot(ax=plt.gca(), legend=False, alpha=0.6) 
plt.title('Registration Trends for All Countries (3-Year Moving Average)')
plt.xlabel('Year')
plt.ylabel('Registrations')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('all_countries_trends.png')

print("Process Complete for all countries.")