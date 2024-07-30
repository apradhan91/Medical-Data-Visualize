import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# imports data
df = pd.read_csv("medical_examination.csv")

# add the overweight column
df['overweight'] = (df["weight"]/ ((df["height"] / 100)**2 )).apply(lambda x: 1 if x>25 else 0)

# Normalize data by making 0 always good and 1 always bad. if the value of 'cholestrol' or 'gluc' is 1, make the value 0, if the value is more than 1, make the value 1
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x==1 else 1)


# Draw categorical plot
def draw_cat_plot():
    # create dataframe for cat plot using pd.melt' using just the values from 'cholesterol', 'gluc','smoke', 'alco', 'active', and 'overweight' (values are either 0 or 1). 
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars= ['cholesterol', 'gluc','smoke', 'alco', 'active', 'overweight'])

 
    # group and reformat the data to split it by cardio, Show the counts of each feature. 
    df_cat["total"] = 1
    df_cat = df_cat.groupby(["cardio", "variable", "value"], as_index=False).count() #changed default to false
    

    # draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x = "variable", y = "total", data = df_cat, hue="value", kind="bar", col="cardio").fig 

    fig.savefig('catplot.png')
    return fig
 

# Draw Heat Map
def draw_heat_map():
    # clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) 
    ]

    # Calculate correlation matrix
    corr = df_heat.corr(method="pearson")

    # generate a mask for the upper triangle
    mask = np.triu(corr)

    # set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,12))

    # draw the heatmap with sns.heatmap()
    sns.heatmap(corr, linewidths=1, annot=True, square=True, mask=mask, fmt=".1f", center=0.08, cbar_kws= {"shrink":0.5})

    # 16
    fig.savefig('heatmap.png')
    return fig
