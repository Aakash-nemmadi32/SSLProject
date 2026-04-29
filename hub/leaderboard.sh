#!/bin/bash

# clear the csv files before writing fresh data
> connect4.csv
> tictactoe.csv
> othello.csv

# associative arrays to hold win/loss counts per player per game
declare -A connect4_win
declare -A tictactoe_win
declare -A connect4_lose
declare -A tictactoe_lose
declare -A othello_win
declare -A othello_lose

# convert history.csv to a space-separated file and strip windows carriage returns
sed 's/,/ /g; s/\r//' history.csv > data.txt

export_to_csv() {
    local game="$1"
    local -n win_local="${game}_win"
    local -n lose_local="${game}_lose"
    local -A seen   # track players we've already written so no duplicates

    for key in "${!win_local[@]}" "${!lose_local[@]}"; do
        # skip if we already processed this player
        [[ -n "${seen[$key]}" ]] && continue
        seen[$key]=1

        local wins=${win_local[$key]:-0}
        local loses=${lose_local[$key]:-0}

        # avoid division by zero — if no losses, ratio is infinity
        if (( loses == 0 )); then
            local ratio_sort="99999"   # high number so inf sorts to the top
            local ratio="inf"
        else
            local ratio=$(echo "scale=2; $wins / $loses" | bc -l)
            local ratio_sort="$ratio"
        fi
        [[ $loses == 0 ]] && ratio="inf"

        echo "$key,$wins,$loses,$ratio_sort,$ratio"
    done >> "${game}.csv"
}

# pretty prints a game's txt file as an aligned table
print_table() {
   awk -F ","  '
  
 { data[NR]=$0
   # track the longest username and win/lose ratio for column width
   if (length($1) > max) max = length($1)
   if (length($5) > max5) max5 = length($5)
 }
END {
  # minimum column widths so the header fits
  if ( max5 < 8 ) max5 = 8
  if (max < 8) max = 8

  sep = max + max5 + 22    # total separator line length

  # header row
  printf "| %-*s | %4s | %5s | %-*s |\n", max, "Username", "Wins", "Loses", max5 , "Win/Lose"

  # separator line
  for (i=1; i<=sep; i++) printf "-"
  printf "\n"

  # one row per player
  for (i=1; i<=NR; i++) {
    split(data[i], f, ",")
    printf "| %-*s | %4s | %5s | %-*s |\n", max, f[1], f[2], f[3], max5 , f[5]
  }
}
' "$1.txt"
}


# read through every match in history and tally wins and losses
while read -r line || [[ -n "$line" ]]; do
    x=($line)

    # x[0]=winner  x[1]=loser  x[3]=game name
    if [[ "${x[3]}" == "connect4" || "${x[3]}" == "tictactoe" || "${x[3]}" == "othello" ]]; then
        (( ${x[3]}_win["${x[0]}"]++ ))
        (( ${x[3]}_lose["${x[1]}"]++ ))
    fi

done < data.txt

# write the tallied data out to each game's csv
export_to_csv connect4
export_to_csv tictactoe
export_to_csv othello

# sort each game's csv based on the flag passed in and save to a txt for printing
games=( "connect4" "othello" "tictactoe" )
for game in "${games[@]}" ; do
    if [[ "$1" == "username" ]]; then
        sort -t "," -k1 -f "${game}.csv" > "${game}.txt"          # alphabetical
    elif [[ "$1" == "Wins" ]]; then
        sort -t "," -k2 -rn "${game}.csv" > "${game}.txt"         # most wins first
    elif [[ "$1" == "Loses" ]]; then
        sort -t "," -k3 -rn "${game}.csv" > "${game}.txt"         # most losses first
    elif [[ "$1" == "Wins/Loses" ]]; then
        sort -t "," -k4 -rn "${game}.csv" > "${game}.txt"         # best ratio first
    fi
done

# print all three leaderboards
echo ""
echo "======================Connect4========================="
print_table connect4
echo "========================================================"
echo ""
echo "TicTacToe"
print_table tictactoe
echo "========================================================"
echo ""
echo "Othello"
print_table othello