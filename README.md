# Twitter-API-Mariners-Post

I'm a huge baseball fan and an even bigger Seattle Mariners fan. In the 2018 season, I started a thread of the team's W-L 
record starting with 162-0 (I can dream). Each loss meant I would add to the tweet with a minus in the win column and a plus 
to the loss column. This season I changed it up with a thread that started at 0-0, meaning I tweet the results of each game. 
162 games means 162 tweets which can get tiresome. This is where I thought to make this process simpler.

For this project I used Twitter's API where I would tell my program if the Mariners won or lost that game. My program would
then find the last tweet of the on-going thread and tweet with the updated record.

I chose to implement this program to first reading a text file that consisted of the most recent tweet's ID, the current wins,
and the current loses. The text file could have instead kept record of only the most recent tweet's ID and grab the wins and
loses from that tweet but I didn't want to waste time of parsing through that tweet. 

Here are the steps my program takes:
  1. Authenticate consumer and access keys
  2. Create window
  3. Read information from text file
  4. Add labels and buttons to the window
  5. Wait for user input indicating whether the team won or lost
  6. Increment win/lose
  7. Tweet updated record to previous tweet
  8. Write to text file the new tweet's ID and the updated win/lose
  9. Open a tab to the new tweet
  10. Close window
