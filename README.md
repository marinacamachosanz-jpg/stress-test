```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto
```

```bash
uv pip install hf_transfer
hf auth login
```

```bash
vllm serve meta-llama/Llama-3.1-70B-Instruct --tensor-parallel-size 4 --max-model-len 4096
```

```bash
vllm bench serve --backend vllm --model meta-llama/Llama-3.1-70B-Instruct --endpoint /v1/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 64
```

```bash
streamlit run app.py
```