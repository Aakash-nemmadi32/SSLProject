#!/bin/bash
#assuming that what field is selected is given as a command-line argument
opt=$1
#creating files to store data
touch temp.csv ttemp.csv
#writing heading in temp.csv
echo "Player Name,Total Number of games player played,Number of games player won,Number of games player lost,Ratio of number of wins and losses" >> temp.csv
#Using Awk command to extract fields in history.csv and count
awk -F "," '
BEGIN{
	OFS = ",";
}
{
	if ( NR > 1 ) {
		#Ignoring first line and incrementing repectives players number of wins and losses using associative arrays
		winner = $3;
		loser = $4;
		Wins[winner]++;
		Losses[loser]++;
		Total[winner]++;
		Total[loser]++;}
	}
END{    #adding unsorted to ttemp.csv
	for (p in Total){
		k = Wins[p]/Losses[p];
		print p, Total[p], Wins[p], Losses[p], k }  
	}' history.csv >> ttemp.csv
#sorting data based on given command-line argument
if [[ "$opt" == "Sort by Wins"  ]];then 
	sort -t "," -k3,3rn ttemp.csv >> temp.csv
elif [[ "$opt" == "Sort by Losses" ]]; then
	sort -t "," -k4,4rn ttemp.csv >> temp.csv
else
	sort -t "," -k5,5rn ttemp.csv >> temp.csv
fi
#printing final resulting table
awk 'BEGIN{ FS = ","; OFS = " "; RS = "\n"; ORS = "\n"; }{print $1,$2,$3,$4,$5}' temp.csv
#removing the created files
rm temp.csv ttemp.csv
