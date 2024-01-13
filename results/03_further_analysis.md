# Further Analysis

Following this we try to remove any data that wont help in generating the model

THis includes
* Players that have an average play time below a certain threshold

When checking these we can see that there are a lot of players who never play! THis makes sense when you consider that there are 20 teams each with 11 players each ~200 players. obviously there are subs and team changes so we can go to 4-500. SO ~16 players that never play is feesable.

We will atleast remove the players with 0 mins and for now, below 1 standard deviation.

![Example Image](../resources/av_mins_per_player.png)

After removing, we get a distribution like this:

![Example Image](../resources/av_pp_after_cut.png)

However if we look at the minutes distribution, we still have too much 0 data

![Example Image](../resources/mins_after_cut.png)

If we remove below the average we get something closer to reasonable:

![Example Image](../resources/mins_after_av_rmv.png)

