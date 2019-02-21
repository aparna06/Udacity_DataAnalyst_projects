---
title: "README"
author: "Aparna Radhakrishnan"
date: "1/23/2019"
output: html_document
---

## Summary
Using the baseball data statistics of the average batting and number of home runs of 70 baseball players, a scatter plot was created. However, 22 of them had 0 for average batting and home runs. I have converted the height to meter and weight to kilograms and calculated BMI. The left handed players had a mean batting average that was around the 0.26. While for the right handed players the mean batting average was lesser but more spread out. The data for dual handed players were two few to comment. The BMI did not seem to have much effect on the player statistics.

## Design explain any design choices you made including changes to the visualization after collecting feedback
I did a scatter plot of average batting versus home runs for each players used the BMI for the size of the circle and handedness for colour.

I created four buttons - Left, Right, Both and All. I also created an alert to click the buttons to urge users to explore data more.

I further attached tooltips that returns the name and BMI of the player when hovered on the point.


## Feedback
My first two sketches was done in R while I was exploring the data. Please look at the ExploringBaseBallData.html.

My first plot :**index.html**

*Afterthought:* While interacting the data, I realised I wanted to look the plot with all the data as well. 
*Follow-up:* So I created a fourth button for the same which resulted in **index2.html**

*Feedback:* The effect of BMI was not clear in the size of the points.
*Follow-up:* I used the range of precalculated BMI (this dataset with BMI and ordering was done in R exploration) to replot the data. This resulted in **index3.html**.

*Feeback:* The buttons did not seem obvious to click.
*Follow-up:* I created an alert button to explain to the user what could do next. This was compiled in **index4.html**.

*Feedback:* The user wished to know the name of the players that were there in the outliers. 
*Follow-up:* I attached the tooltip function to each point with the name and BMI of the player. This was compiled in **index5.html**.

*Feedback:* It is not clear what defined the sizes or the values in the tooltip. 
*Follow-up:* I added "BMI=" in the tooltip and a legend for size resulting in **index6.html**

*Submission Feedback:* The mean average batting is not clear. 
*Follow-up:* I added a cross to represent the mean for each group. This was compiled as the final html **index_final.html**.


## Resources
Data: https://s3.amazonaws.com/udacity-hosted-downloads/ud507/baseball_data.csv
Update: https://bl.ocks.org/mbostock/3808218

Tooltip : https://stackoverflow.com/questions/10805184/show-data-on-mouseover-of-circle
          https://stackoverflow.com/questions/29194507/why-do-i-get-a-uncaught-typeerror-when-i-introduce-a-d3-transition
          
Formatting : https://github.com/d3/d3-format

D3 Symbols for mean: https://bl.ocks.org/d3indepth/bae221df69af953fb06351e1391e89a0
https://stackoverflow.com/questions/42720913/how-can-i-set-the-size-of-my-d3-symbols-size-isnt-working-for-me




