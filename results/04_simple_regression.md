# Simple Regression

Now that we have our data, we start with some simpler regression models. Our data consists of 4 previous fixtures, trying to predict the total of the next three fixtures as we are looking for medium term performance of the players.

# Random forest

After testing a range of parameters from a subset of the data we find the the best model so far can produce an R^2 value of 0.6. Not bad!

Minutes played, points and value from the previous week are the most important feautures suggesting not much can be gained linearly from the previous weeks performance.

![Example Image](../resources/best_initial_random_forest.png)

From here we try predicting 1 fixture from 2 and 10 fixtures from 11. Trying to get the exact score from the previous two games is unsurprisingly difficult and we only see an R^2 of 0.2

![Example Image](../resources/rf_1day.png)

Using the previous 11 to predict sum of 10 fixtures we get an R^2 of around 0.5 so slightly worse again. Seems like predicting 3 games could be a good middle ground. I may test this further at a later date

![Example Image](../resources/rf_10day.png)

