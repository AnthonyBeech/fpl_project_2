# Initial Analysis of raw data

This document is the first 9very rough look at the cleaned data to be used for building the model! We have 85728 rows of data from a range of years but are only using players currently in the API (~800 players).

## Looking at the distribution of each column and the correlation with points

Firstly we plot each of the columns to see what were working with and what we wll keep for further analysis.

https://github.com/AnthonyBeech/fpl_project_2/blob/main/resources/distribution_of_points.png?raw=true

![Example Image](./resources/raw_data_all_plots.png)

### Checking some plots in more detail

There are a number of interesting findings here. Firstly the distribution of points. There is an overwheling proportion of data where no points are scored. This is likely players that are rarely played and may well skew the data, so we may need to remove some of this from the later training.

![Example Image](./resources/distribution_of_points.png)

Similarly with minutes, we see that there are many rows where the minutes played is 0, meaning the player did not play at all. Likely these will correlate with scoring zero points. Perhaps removing players by an average minutes played threshold will work well

![Example Image](./resources/minutes_dist.png)

The distribution of kickoff data clearly shows the gaps between seasons and the fact the most data is recent as players slowly leave the league and new players join through the years

![Example Image](./resources/kickoff_dist.png)

When looking at position data, there is little correlation and this shows the importance of onehot encoding for catagorical data. if you were treat the data as numerical, you would likey be losing information in regression analysis.

![Example Image](./resources/position_vs_points.png)

The is an unsurprising correlation between player value and points but it's not but the sd is larger than expected as we see plenty of valueable players with high scores and vice-versa.

![Example Image](./resources/value_vs_points.png)

ICT index (a combination of three headers) has a strong correlation with points although with some sd. Influence takes into account events and actions that could directly or indirectly effect the match outcome. Creativity assesses player performance in terms of producing goal scoring opportunities for others. Threat is the third measure, producing a value that examines a player’s threat on goal; it therefore gauges those individuals most likely to score goals.

![Example Image](./resources/ict_vs_points.png)

Interetingly enough there is amost no difference in performance when home or away!

![Example Image](./resources/home_vs_points.png)

Finally bonus points generally has a good correlation but with some funkyness?

![Example Image](./resources/bps_vs_points.png)


