def scatter(df_plot, impath):

    # Labels to stirngs
    df_plot['labels'] = df_plot['labels'].astype('str')

    # For dot size
    df_plot['log_retweet'] = df_plot['retweet_count'].apply(
        lambda x: np.log(x+2))

    # Remove unclustered tweets
    df_plot = df_plot[df_plot['labels'] != '-1']

    # If too many clusters, only plot the bigger ones.
    if len(set(df_plot['labels'])) > 10:
        top = list(df_plot['labels'].value_counts()[:10].index)
        mapit = [x in top for x in df_plot['labels']]
        df_plot = df_plot[mapit]

    # Create scatter visualization
    fig = px.scatter(df_plot, x="x", y="y", color='labels',
                        size='log_retweet', hover_name='text',
                        title='Clusters of tweets with similar meaning')

    # Save dataviz
    plotly.offline.plot(fig, filename=impath)