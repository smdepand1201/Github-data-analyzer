import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# SUST Template Font Compliance
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'figure.dpi': 100
})

downloads_path = os.path.expanduser("~/Downloads/thesis")
file_path = os.path.join(downloads_path, "repo_bots.csv")
df = pd.read_csv(file_path)

df['Automation Group'] = pd.cut(
    df['Automation Files'],
    bins=[-1, 0, 9, np.inf],
    labels=['No Automation', 'Moderate (1-9)', 'High (10+)']
)

# Clustering
X = df[["Automation Files", "Commits (30 days)"]]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X)

cluster_labels = {
    0: "Low Automation, High Activity",
    1: "Moderate Automation, Moderate Activity",
    2: "High Automation, Low Activity"
}
df["Cluster Label"] = df["Cluster"].map(cluster_labels)

plt.figure(figsize=(8, 6))
scatter = sns.scatterplot(
    data=df,
    x="Automation Files",
    y="Commits (30 days)",
    hue="Cluster Label",
    palette="viridis",
    alpha=0.7,
    s=80
)
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    c="red",
    marker="X",
    s=200,
    label="Centroids"
)
sns.regplot(
    data=df,
    x="Automation Files",
    y="Commits (30 days)",
    scatter=False,
    color='black',
    line_kws={'linestyle': '--', 'label': 'Overall Trend'}
)
plt.xlabel("Number of Automation Files", fontweight='bold')
plt.ylabel("Contributor Activity (Commits/30 Days)", fontweight='bold')
plt.title("Clustering of Repositories by Automation and Activity", fontsize=14)
plt.legend(title="Cluster Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("clustering_repositories.png")
plt.show()

# Heatmap Common
corr_matrix = df[[
    "Automation Files",
    "Rejection Rate (%)",
    "Avg. Merge Time (hours)",
    "Avg. Resolution Time (hours)",
    "Stars"
]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    mask=np.triu(np.ones_like(corr_matrix, dtype=bool)),
    linewidths=0.5
)
plt.title("Correlation Heatmap of Key Metrics", fontsize=14)
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()

# Issue vs Automation
plt.figure(figsize=(8, 6))
scatter = sns.scatterplot(
    data=df,
    x="Automation Files",
    y="Avg. Resolution Time (hours)",
    hue="Project Type",
    palette="Set1",
    alpha=0.7,
    edgecolor='black',
    s=80
)
for pt, color in zip(['Open Source', 'Mixed'], ['#1f77b4', '#ff7f0e']):
    sns.regplot(
        data=df[df['Project Type'] == pt],
        x="Automation Files",
        y="Avg. Resolution Time (hours)",
        scatter=False,
        line_kws={'color': color, 'linestyle': '--', 'label': f'{pt} Trend'}
    )
plt.xlabel("Number of Automation Files", fontweight='bold')
plt.ylabel("Issue Resolution Time (Hours)", fontweight='bold')
plt.title("Automation vs. Issue Resolution Time by Project Type", fontsize=14)
plt.legend(title="Project Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("issue_resolution_time.png")
plt.show()

# PR rejection rate
plt.figure(figsize=(8, 6))
ax = sns.barplot(
    data=df,
    x="Automation Group",
    y="Rejection Rate (%)",
    hue="Project Type",
    errorbar=('ci', 95),
    palette="Set2",
    err_kws={'linewidth': 1.5},
    capsize=0.1
)

# Trend line
trend_data = {'Open Source': {'x': [], 'y': []}, 'Mixed': {'x': [], 'y': []}}
automation_order = df['Automation Group'].cat.categories.tolist()

for i, group in enumerate(automation_order):
    for j, pt in enumerate(['Open Source', 'Mixed']):
        subset = df[(df['Automation Group'] == group) & (df['Project Type'] == pt)]
        if not subset.empty:
            x_pos = i + (-0.2 + j*0.4)
            trend_data[pt]['x'].append(x_pos)
            trend_data[pt]['y'].append(subset['Rejection Rate (%)'].mean())

colors = [ax.containers[0][0].get_facecolor(), ax.containers[1][0].get_facecolor()]
for idx, pt in enumerate(['Open Source', 'Mixed']):
    sorted_data = sorted(zip(trend_data[pt]['x'], trend_data[pt]['y']), key=lambda x: x[0])
    x_vals = [x for x,y in sorted_data]
    y_vals = [y for x,y in sorted_data]
    ax.plot(x_vals, y_vals, color=colors[idx], linestyle='--', 
            marker='o', markersize=8, linewidth=2, label=f'{pt} Trend')

handles, labels = ax.get_legend_handles_labels()
new_handles = handles + [
    plt.Line2D([0], [0], color=colors[0], linestyle='--', linewidth=2),
    plt.Line2D([0], [0], color=colors[1], linestyle='--', linewidth=2)
]
plt.legend(handles=new_handles, title="Project Type", loc='upper right')
plt.xlabel("Automation Level", fontweight='bold')
plt.ylabel("Rejection Rate (%)", fontweight='bold')
plt.title("Pull Request Rejection Rate by Automation Level", fontsize=14)
plt.tight_layout()
plt.savefig("pr_rejection_rate.png")
plt.show()

# Repo distribution
repo_dist = df.groupby(["Project Type", "Automation Group"], observed=False).size().unstack()
repo_dist = repo_dist.div(repo_dist.sum(axis=1), axis=0) * 100

plt.figure(figsize=(8, 6))
repo_dist.plot(
    kind="bar",
    stacked=True,
    color=["#1f77b4", "#ff7f0e", "#2ca02c"],
    edgecolor='black'
)
plt.xlabel("Project Type", fontweight='bold')
plt.ylabel("Percentage of Repositories (%)", fontweight='bold')
plt.title("Repository Distribution by Automation Level", fontsize=14)
plt.legend(title="Automation Group", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("repo_distribution.png")
plt.show()

# Merge vs Automation
plt.figure(figsize=(8, 6))
ax = sns.barplot(
    data=df,
    x="Automation Group",
    y="Avg. Merge Time (hours)",
    hue="Project Type",
    errorbar=('ci', 95),
    palette="Set1",
    err_kws={'linewidth': 1.5},
    capsize=0.1
)

# Outlier detection
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df,
    x="Stars",
    y="Forks",
    size="Rejection Rate (%)",
    hue="Project Type",
    palette="Set1",
    sizes=(20, 200),
    alpha=0.7,
    edgecolor='black'
)

# Trendlines once more
for pt, color in zip(['Open Source', 'Mixed'], ['#1f77b4', '#ff7f0e']):
    sns.regplot(
        data=df[df['Project Type'] == pt],
        x="Stars",
        y="Forks",
        scatter=False,
        color=color,
        line_kws={'linestyle': '--', 'label': f'{pt} Trend'}
    )

plt.axvline(x=50000, color='red', linestyle='--', label="High Stars Threshold (50k)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel("GitHub Stars", fontweight='bold')
plt.ylabel("Forks", fontweight='bold')
plt.title("Outlier Detection: High-Stars Repositories", fontsize=14)
plt.tight_layout()
plt.savefig("outlier_detection.png")
plt.show()
