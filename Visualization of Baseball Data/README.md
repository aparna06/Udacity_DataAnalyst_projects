---
title: "README"
author: "Aparna Radhakrishnan"
date: "1/23/2019"
output: html_document
---

## Summary
Using the baseball data statistics of the average batting and number of home runs of 70 baseball players, a scatter plot was created. However, 22 of them had 0 for average batting and home runs. I have converted the height to meter and weight to kilograms and calculated BMI. The left handed players had a batting average that was around the 0.25 mark while for the right handed players the average was more spread out.

## Design explain any design choices you made including changes to the visualization after collecting feedback
I did a scatter plot of average batting versus home runs for each players used the BMI for the size of the circle and handedness for colour.

I created four buttons - Left, Right, Both and All. I also created an alert to click the buttons to urge users to explore data more.

I further attached tooltips that returns the name and BMI of the player when hovered on the point.


## Feedback
My first two sketches was done in R while I was exploring the data. Please look at the ExploringBaseBallData.html.

**index.html** was my first go at the plot. While looking at it, I realised I wanted to look the plot with all the data as well. So I created a fourth button for the same which resulted in **index2.html**

On receiving feedback about the radius of the circle, I used the range of precalculated BMI (this dataset with BMI and ordering was done in R exploration) to replot the data. This resulted in **index3.html**.

When I did send out the visualisation for feedback, the buttons did not seem obvious to click so I created an alert button to explain to the user what could be done next.

The after thought was then compiled in **index4.html**.

The visualisation (index4.html) was sent for feedback and the user wished to know the name of the players that were there in the outliers. For this feedback, I attached the tooltip function to each point with the name and BMI of the player.

This was then compiled in **index5.html**.

The visualisation (index5.html) was sent for feedback and it was not clear to the user what defined the sizes or the values in the tooltip. This, I added "BMI=" in the tooltip and a legend for size.

This was then compiled as the final html **index_final.html**.


## Resources
Data: https://s3.amazonaws.com/udacity-hosted-downloads/ud507/baseball_data.csv
Update: https://bl.ocks.org/mbostock/3808218

Tooltip : https://stackoverflow.com/questions/10805184/show-data-on-mouseover-of-circle
          https://stackoverflow.com/questions/29194507/why-do-i-get-a-uncaught-typeerror-when-i-introduce-a-d3-transition
          
Formatting : https://github.com/d3/d3-format



