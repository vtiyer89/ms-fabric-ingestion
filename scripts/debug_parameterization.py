"""Locally validate this workspace's parameter.yml against the repo — no Fabric API calls,
no credentials needed. Confirms/denies: file_path and item_type/item_name filters actually
match real files, find_value strings are actually found in those files, and the whole file
passes schema validation. Does NOT resolve $workspace./$items. dynamic variables (that needs
a live, credentialed run — see debug_live_test.py for that).

Run: pip install -r scripts/requirements.txt && python scripts/debug_parameterization.py
"""

from pathlib import Path

from fabric_cicd import change_log_level
from fabric_cicd._parameter._utils import validate_parameter_file

# See every match/skip decision, not just pass/fail
change_log_level("DEBUG")

root_directory = Path(__file__).resolve().parent.parent
repository_directory = str(root_directory / "datasource_nyc_taxi")

result = validate_parameter_file(
    repository_directory=repository_directory,
    item_type_in_scope=["Lakehouse", "DataPipeline", "CopyJob"],
    environment="TEST",
)

print(f"\nvalidate_parameter_file returned: {result}")
