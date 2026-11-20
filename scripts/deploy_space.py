"""Deploy UTM PageRank Research Workbench to Hugging Face Spaces."""

from pathlib import Path

from huggingface_hub import HfApi

REPO_ROOT = Path(__file__).resolve().parent.parent
SPACE_DIR = REPO_ROOT / "deploy" / "hf_space"
REPO_ID = "Rhindottire/UTM-PageRank"


def deploy() -> None:
    api = HfApi()
    user_info = api.whoami()
    username = str(user_info.get("name") or "Rhindottire")
    print(f"[1/3] Logged in to Hugging Face as: {username}")

    print(f"[2/3] Creating / checking Space repository: {REPO_ID} (Docker SDK)...")
    api.create_repo(
        repo_id=REPO_ID, repo_type="space", space_sdk="docker", exist_ok=True
    )

    print(f"[3/3] Uploading deployment artifacts from {SPACE_DIR}...")
    api.upload_folder(
        folder_path=str(SPACE_DIR),
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="Deploy UTM Web Graph & PageRank Intelligence (PPW Task 7)",
    )

    runtime = api.get_space_runtime(repo_id=REPO_ID)
    print("\n✅ Deployment successful!")
    print(f"Stage: {runtime.stage}")
    print(f"Public URL: https://{username.lower()}-utm-pagerank.hf.space")


if __name__ == "__main__":
    deploy()
