import sqlite3

import matplotlib.pyplot as plt

# SQLiteデータベースに接続
conn = sqlite3.connect("../outputs/ring.sqlite")
c = conn.cursor()

# プロットの設定
fig = plt.figure(figsize=(20, 10))
freq_ranges = ["Low (0-20Hz)", "Mid (20-100Hz)", "High (100-300Hz)"]
gap_junction_labels = ["Without Gap Junction", "With Gap Junction"]

for i, freq_range in enumerate(freq_ranges):
    for j, gap_junction in enumerate([0, 1]):
        ax = fig.add_subplot(2, 3, 1 + i + j * 3, projection="3d")

        # 条件に合致するデータを取得するSQL文
        query = f"""
        SELECT n_cells, connectivity, frequency, low, mid, high
        FROM jobs
        WHERE with_gap_junctions = {gap_junction}
        """

        # データの取得
        c.execute(query)
        plot_data = c.fetchall()

        if len(plot_data) > 0:
            # 軸の設定
            ax.set_xlabel("n_cells")
            ax.set_ylabel("connectivity")
            ax.set_zlabel("frequency")
            ax.set_title(f"{freq_range} - {gap_junction_labels[j]}")

            # カラーマップの設定
            cmap = plt.cm.viridis
            colors = cmap([row[3 + i] for row in plot_data])

            print(plot_data[0])
            # 3次元プロット
            sc = ax.scatter([row[0] for row in plot_data], [row[1] for row in plot_data], [row[2] for row in plot_data], c=colors, cmap=cmap, s=50)

            # カラーバーの設定
            cbar = plt.colorbar(sc, ax=ax)
            cbar.set_label("Max Power Spectral Density")
        else:
            ax.set_title(f"{freq_range} - {gap_junction_labels[j]}\nNo data")

plt.tight_layout()
plt.show()

# データベースを閉じる
conn.close()
