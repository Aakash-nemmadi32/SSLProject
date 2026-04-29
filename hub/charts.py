import matplotlib.pyplot as plt

counts = {"connect4": 0, "tictactoe": 0, "othello": 0}
player_count = {}
lose_count = {}

with open("history.csv") as f:
    rows = [tuple(l.strip().split(",")) for l in f.readlines()]  # list, not set

for row in rows:
    if row[3] in counts:
        counts[row[3]] += 1
    player_count[row[0]] = player_count.get(row[0], 0) + 1
    lose_count[row[1]]   = lose_count.get(row[1], 0) + 1

top5   = sorted(player_count.items(), key=lambda x: x[1], reverse=True)[:5]
worst5 = sorted(lose_count.items(),   key=lambda x: x[1], reverse=True)[:5]

best_players,  best_values  = zip(*top5)   if top5   else ([], [])
worst_players, worst_values = zip(*worst5) if worst5 else ([], [])

fig = plt.figure(figsize=(5, 5), dpi=100)  # exactly 500x500px

# Top row: two bar charts side by side
ax1 = fig.add_subplot(2, 2, 1)
ax1.bar(best_players, best_values, color="green")
ax1.set_title("Top 5 Best Players", fontsize=8)
ax1.tick_params(axis='x', labelsize=6)
ax1.tick_params(axis='y', labelsize=6)

ax2 = fig.add_subplot(2, 2, 2)
ax2.bar(worst_players, worst_values, color="red")
ax2.set_title("Top 5 Worst Players", fontsize=8)
ax2.tick_params(axis='x', labelsize=6)
ax2.tick_params(axis='y', labelsize=6)

# Bottom row: pie chart spanning both columns
ax3 = fig.add_subplot(2, 1, 2)
ax3.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%',
        explode=(0.1, 0, 0), textprops={'fontsize': 7})
ax3.set_title("Games Played", fontsize=8)

plt.tight_layout(pad=1.0)
plt.savefig("Statistics.png", dpi=100)
