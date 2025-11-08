from huggingface_hub import create_repo, upload_folder

repo_id = "TADSTech/financial-news-classifier"
local_model_path = "src/model/saved/finbert/"

create_repo(repo_id, private=False, exist_ok=True)
upload_folder(
    repo_id=repo_id,
    folder_path=local_model_path,
    commit_message="Upload trained financial sentiment model"
)
print(f"Model uploaded successfully to https://huggingface.co/{repo_id}")
