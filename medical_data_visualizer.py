import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv', index_col=0)

# Add 'overweight' column

bmi = df['weight']/((df['height']/100)**2)

df['overweight'] = bmi > 25
df.loc[df['overweight'] == True, 'overweight'] = 1
df.loc[df['overweight'] == False, 'overweight'] = 0
df['overweight'] = df['overweight'].astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df['cholesterol'] == 1, 'cholesterol' ] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol' ] = 1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(frame=df, id_vars='cardio', value_vars = ['active','alco','cholesterol', 'gluc','overweight','smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat.groupby('cardio').value_counts()
    

    # Draw the catplot with 'sns.catplot()'

    sns.catplot(df_cat, kind = 'count', x = 'variable', hue='value', col='cardio')

    # Get the figure for the output
    fig = sns.catplot(df_cat, kind = 'count', x = 'variable', hue='value', col='cardio')


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.copy()
    df_heat = df_heat.loc[df['ap_lo'] <= df['ap_hi']]
    df_heat = df_heat.loc[df['height'] >= df['height'].quantile(0.025)]
    df_heat = df_heat.loc[df['height'] <= df['height'].quantile(0.975)]
    df_heat = df_heat.loc[df['weight'] >= df['weight'].quantile(0.025)]
    df_heat = df_heat.loc[df['weight'] <= df['weight'].quantile(0.975)]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig, ax = fig, ax = plt.subplots(1,1, figsize=[14,12])

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr.round(1), mask=mask, vmax= 0.7, vmin=-0.1, center=0, annot=True, ax=ax, square=True)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
