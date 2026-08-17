"""Locally run the real deploy against Test, authenticated as *you* instead of the SPN —
for fast iteration without waiting on a GitHub Actions round-trip. Requires `az login` first
(uses your own Entra account, so you need at least Contributor on the target Test workspace
yourself — the same access the SPN has).

Setup:
    az login
    pip install -r scripts/requirements.txt
    python scripts/debug_live_test.py
"""

from pathlib import Path

from azure.identity import AzureCliCredential
from fabric_cicd import FabricWorkspace, change_log_level, publish_all_items

change_log_level("DEBUG")

root_directory = Path(__file__).resolve().parent.parent
repository_directory = str(root_directory / "datasource_nyc_taxi")

# Fill in the real Test Ingestion (ws-test-landing-rjoose-v2) workspace ID
WORKSPACE_ID = "e9472408-b9e1-45ae-8c2a-e22911c8b109"

target_workspace = FabricWorkspace(
    workspace_id=WORKSPACE_ID,
    environment="TEST",
    repository_directory=repository_directory,
    item_type_in_scope=["Lakehouse", "DataPipeline", "CopyJob"],
    token_credential=AzureCliCredential(),
)

publish_all_items(target_workspace)
# Deliberately not calling unpublish_all_orphan_items here — this script is for iterating on
# find_replace resolution, not for full deploy parity. Use the real GitHub Actions workflow
# for that once this confirms the parameterization itself is correct.
