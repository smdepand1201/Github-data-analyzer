import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}

REPOSITORIES = [
 "kubernetes/kubernetes",
"apache/spark",
"Microsoft/vscode",
"NixOS/nixpkgs",
"rust-lang/rust",
"firehol/blocklist-ipsets",
"openshift/origin",
"ansible/ansible",
"Automattic/wp-calypso",
"Microsoft/dotnet",
"tensorflow/tensorflow",
"elastic/elasticsearch",
"apple/swift",
"hashicorp/terraform",
"prometheus/prometheus",
"grafana/grafana",
"jenkinsci/jenkins",
"apache/kafka",
"istio/istio",
"helm/helm",
"spinnaker/spinnaker",
"hashicorp/consul",
"hashicorp/vault",
"apache/airflow",
"saltstack/salt",
"puppetlabs/puppet",
"chef/chef",
"travis-ci/travis-ci",
"circleci/circleci-docs",
"drone/drone",
"gitlabhq/gitlabhq",
"argo-cd/argo-cd",
"fluxcd/flux",
"tektoncd/pipeline",
"concourse/concourse",
"spiffe/spire",
"open-policy-agent/opa",
"kyverno/kyverno",
"openfaas/faas",
"serverless/serverless",
"pulumi/pulumi",
"crossplane/crossplane",
"openstack/openstack",
"ceph/ceph",
"rook/rook",
"kubeflow/kubeflow",
"mlflow/mlflow",
"ray-project/ray",
"prefecthq/prefect",
"dagster-io/dagster",
"dvcorg/dvc",
"jupyter/notebook",
"apache/beam",
"open-telemetry/opentelemetry-collector",
"jaegertracing/jaeger",
"grafana/loki",
"fluent/fluentd",
"vectorizedio/redpanda",
"materializeinc/materialize",
"questdb/questdb",
"timescale/timescaledb",
"influxdata/influxdb",
"prometheus/alertmanager",
"grafana/agent",
"cortexproject/cortex",
"thanos-io/thanos",
"observatorium/observatorium",
"open-telemetry/opentelemetry-collector-contrib",
"open-telemetry/opentelemetry-java",
"open-telemetry/opentelemetry-go",
"open-telemetry/opentelemetry-python",
"open-telemetry/opentelemetry-js",
"open-telemetry/opentelemetry-dotnet",
"open-telemetry/opentelemetry-cpp",
"open-telemetry/opentelemetry-rust",
"open-telemetry/opentelemetry-php",
"open-telemetry/opentelemetry-ruby",
"open-telemetry/opentelemetry-swift",
"open-telemetry/opentelemetry-erlang",
"open-telemetry/opentelemetry-node",
"open-telemetry/opentelemetry-collector-builder",
"open-telemetry/opentelemetry-operator",
"open-telemetry/opentelemetry-demo",
"open-telemetry/opentelemetry-specification",
"open-telemetry/opentelemetry-proto",
"open-telemetry/opentelemetry-service",
"open-telemetry/opentelemetry-website",
"open-telemetry/opentelemetry-java-instrumentation",
"open-telemetry/opentelemetry-go-contrib",
"open-telemetry/opentelemetry-python-contrib",
"open-telemetry/opentelemetry-js-contrib",
"open-telemetry/opentelemetry-dotnet-instrumentation",
"open-telemetry/opentelemetry-cpp-contrib",
"open-telemetry/opentelemetry-rust-contrib",
"open-telemetry/opentelemetry-php-contrib",
"open-telemetry/opentelemetry-ruby-contrib",
"open-telemetry/opentelemetry-swift-contrib",
"open-telemetry/opentelemetry-erlang-contrib",
"open-telemetry/opentelemetry-node-contrib",
"microsoft/TypeScript",
"vuejs/vue",
"angular/angular",
"pytorch/pytorch",
"facebook/react",
"scikit-learn/scikit-learn",
"flutter/flutter",
"electron/electron",
"numpy/numpy",
"django/django",
"redis/redis",
"opencv/opencv",
"spring-projects/spring-framework",
"jenkinsci/blueocean-plugin",
"apache/zookeeper",
"apache/ignite",
"opensearch-project/OpenSearch",
"apache/camel",
"ansible/awx",
"hashicorp/packer",
"hashicorp/nomad",
"elastic/logstash",
"apache/hudi",
"apache/incubator-doris",
"apache/flink",
"apache/shardingsphere",
"apache/hadoop",
"bentoml/BentoML",
"wandb/client",
"streamlit/streamlit",
"fastapi/fastapi",
"libreoffice/core",
"vercel/next.js",
"gatsbyjs/gatsby",
"twbs/bootstrap",
"pallets/flask",
"pytest-dev/pytest",
"pandas-dev/pandas",
"datafold/data-diff",
"projectmesa/mesa",
"pytest-dev/pytest-django",
"pytest-dev/pytest-xdist",
"kedro-org/kedro",
"open-mmlab/mmdetection",
"huggingface/transformers",
"open-mmlab/mmcv",
"neuralmagic/sparseml",
"explosion/spaCy",
"facebookresearch/fairseq",
"ultralytics/yolov5",
"open-mmlab/mmsegmentation",
"ipython/ipython",
"fastai/fastai",
"pytorch/serve",
"apache/arrow",
"apache/cassandra",
"numpy/numpydoc",
"scipy/scipy",
"tornadoweb/tornado",
"seaborn/seaborn",
"matplotlib/matplotlib",
"sympy/sympy",
"astropy/astropy",
"networkx/networkx",
"dask/dask",
"bokeh/bokeh",
"pytest-dev/pytest-mock",
"pytest-dev/pytest-html",
"pytest-dev/pytest-cov",
"apache/avro",
"apache/thrift",
"apache/tika",
"apache/commons-lang",
"apache/logging-log4j2",
"notebooks/emptyrepo",
"examples/noautomation",
"python-poetry/poetry",
"ethereum/solidity",
"tensorflow/models",
"mozilla/gecko",
"torvalds/linux",
"apache/httpd",
"openssl/openssl",
"python/cpython",
"nodejs/node",
"apache/maven",
"apache/ant"
]
# Function to back off exp.
def fetch_from_api(url):
    retries = 5
    backoff = 1

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:  # Rate limit exceeded
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait_time = max(0, reset_time - int(time.time()))
                print(f"Rate limit exceeded. Retrying after {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Error {response.status_code}: {response.json()} for URL {url}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff *= 2
    print(f"Failed to fetch data from {url} after {retries} retries.")
    return None
#Formulas
def calculate_pr_metrics(pulls):
    merge_times = []
    rejected_count = 0

    for pr in pulls:
        if pr.get('merged_at'):
            created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
            merge_times.append((merged_at - created_at).total_seconds())
        elif pr['state'] == 'closed' and not pr.get('merged_at'):
            rejected_count += 1

    avg_merge_time = sum(merge_times) / len(merge_times) if merge_times else None
    rejection_rate = (rejected_count / len(pulls)) * 100 if pulls else None

    return avg_merge_time, rejection_rate

def calculate_issue_resolution_time(issues):
    resolution_times = []

    for issue in issues:
        if issue['state'] == 'closed':
            created_at = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            closed_at = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            resolution_times.append((closed_at - created_at).total_seconds())

    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else None

    return avg_resolution_time

# Fetch section
def fetch_repo_stats(repo):
    print(f"Fetching stats for {repo}...")
    repo_url = f"https://api.github.com/repos/{repo}"
    workflows_url = f"https://api.github.com/repos/{repo}/contents/.github/workflows"
    pulls_url = f"https://api.github.com/repos/{repo}/pulls?state=all&per_page=100"
    issues_url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100"
    contributors_url = f"https://api.github.com/repos/{repo}/contributors?per_page=100"
    commits_url = f"https://api.github.com/repos/{repo}/commits?since={(datetime.now() - timedelta(days=30)).isoformat()}"

    repo_info = fetch_from_api(repo_url)
    if not repo_info:
        return None

    workflows = fetch_from_api(workflows_url)
    workflow_count = len(workflows) if workflows else 0

    pulls = fetch_from_api(pulls_url)
    avg_merge_time, rejection_rate = calculate_pr_metrics(pulls) if pulls else (None, None)
    open_prs = len([pr for pr in pulls if pr['state'] == 'open']) if pulls else 0
    closed_prs = len([pr for pr in pulls if pr['state'] == 'closed']) if pulls else 0

    issues = fetch_from_api(issues_url)
    avg_resolution_time = calculate_issue_resolution_time(issues) if issues else None
    open_issues = len([issue for issue in issues if 'pull_request' not in issue and issue['state'] == 'open']) if issues else 0
    closed_issues = len([issue for issue in issues if 'pull_request' not in issue and issue['state'] == 'closed']) if issues else 0

    contributors = fetch_from_api(contributors_url)
    contributor_count = len(contributors) if contributors else 0

    commits = fetch_from_api(commits_url)
    commit_count = len(commits) if commits else 0

    return {
        "Repository Name": repo,
        "Project Type"
        "Automation Files": workflow_count,
        "Stars": repo_info.get("stargazers_count", 0),
        "Forks": repo_info.get("forks_count", 0),
        "Project Size (KB)": repo_info.get("size", 0),
        "Commits (30 days)": commit_count,
        "Open PRs (30 days)": open_prs,
        "Closed PRs (30 days)": closed_prs,
        "Open Issues (30 days)": open_issues,
        "Closed Issues (30 days)": closed_issues,
        "Avg. Merge Time (seconds)": avg_merge_time,
        "Rejection Rate (%)": rejection_rate,
        "Avg. Resolution Time (seconds)": avg_resolution_time,
        "Contributors": contributor_count
    }

# Rate limiter
all_repo_data = []
for repo in REPOSITORIES:
    repo_data = fetch_repo_stats(repo)
    if repo_data:
        all_repo_data.append(repo_data)
    time.sleep(1)
df = pd.DataFrame(all_repo_data)
df.reset_index(inplace=True)
df.rename(columns={'index': 'Index'}, inplace=True)
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
thesis_folder = os.path.join(downloads_folder, "thesis")
os.makedirs(thesis_folder, exist_ok=True)
csv_path = os.path.join(thesis_folder, "repo_stats.csv")
df.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")