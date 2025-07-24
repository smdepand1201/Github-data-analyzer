# Github-data-analyzer
This project explores the relationship between automation and contributor activity in popular open-source GitHub repositories. By collecting, cleaning, clustering, and visualizing real data, it uncovers key insights into how automation levels impact repository health, merge times, issue resolution, and PR rejection rates.

Features

- Data Collection: Uses GitHub REST API to fetch repository stats like commits, PRs, issues, stars, forks, and automation files (.github/workflows).
- Clustering & Analysis: Implements KMeans clustering on automation files vs contributor activity to identify usage patterns.
- Visualizations:
  - Repository distribution by automation level
  - Pull request rejection rates across automation categories
  - Issue resolution and merge time comparisons
  - Correlation heatmaps
  - Outlier detection using stars and forks
- Exported Outputs: Cleaned CSV files and high-resolution plots for research or reporting.

Technologies Used

- **Python 3.9+**
- **Pandas, NumPy**
- **Matplotlib, Seaborn**
- **scikit-learn**
- **GitHub API (REST)**

Sample Outputs

Images generated:
- `clustering_repositories.png`
- `correlation_heatmap.png`
- `issue_resolution_time.png`
- `repo_distribution.png`
- `pr_rejection_rate.png`

## 🚀 How to Run

1. Clone the repo
2. Replace the GitHub token in *repocollecter.py
3. Run scripts in sequence:
   python repocollecter.py
   python reponbots.py
   python Newdatavisualization.py
