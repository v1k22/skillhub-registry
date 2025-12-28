---
metadata:
  name: "benchmark-qwen"
  version: "1.0.0"
  description: "Benchmark Qwen 3B model on custom hardware with comprehensive performance metrics"
  category: "benchmarking"
  tags: ["llm", "benchmarking", "qwen", "performance", "ml"]
  author: "skillhub"
  created: "2024-01-15"
  updated: "2025-12-28"

requirements:
  os: ["linux", "macos"]
  python: ">=3.9"
  packages:
    - torch>=2.0.0
    - transformers>=4.35.0
    - datasets
    - pandas
    - matplotlib
  hardware:
    - gpu_memory: ">=8GB"
    - ram: ">=16GB"
    - disk_space: ">=20GB"

estimated_time: "30-45 minutes"
difficulty: "intermediate"
---

# Benchmark Qwen Model

## Overview
This skill benchmarks the Qwen 3B language model on your hardware, providing comprehensive performance metrics including throughput, latency, and memory usage. Perfect for comparing hardware configurations or validating model performance.

## Task Description
Complete end-to-end benchmarking workflow:
1. Set up Python environment with required dependencies
2. Download and cache the Qwen 3B model from HuggingFace
3. Prepare benchmark datasets (MMLU, HellaSwag)
4. Run inference benchmarks with various batch sizes
5. Collect performance metrics (throughput, latency, memory)
6. Generate comprehensive report with visualizations

## Prerequisites
- CUDA-compatible GPU (recommended, will fall back to CPU)
- 20GB free disk space for model and datasets
- Internet connection for model download
- HuggingFace account (optional, for gated models)

## Steps

### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv qwen_bench_env
source qwen_bench_env/bin/activate  # On Windows: qwen_bench_env\Scripts\activate

# Install dependencies
pip install torch transformers datasets pandas matplotlib accelerate
```

### 2. Download Model
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Model configuration
model_name = "Qwen/Qwen-3B"

print(f"Downloading {model_name}...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,  # Use FP16 for efficiency
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

print(f"Model loaded on device: {model.device}")
print(f"Model memory footprint: {model.get_memory_footprint() / 1e9:.2f} GB")
```

### 3. Prepare Benchmark Data
```python
from datasets import load_dataset

# Load standard benchmarks
print("Loading benchmark datasets...")

# MMLU - General knowledge benchmark
try:
    mmlu = load_dataset("cais/mmlu", "all", split="test[:100]")
    print(f"MMLU loaded: {len(mmlu)} samples")
except:
    mmlu = None
    print("MMLU dataset not available, skipping...")

# Create synthetic benchmark data
benchmark_prompts = [
    "Explain quantum computing in simple terms.",
    "Write a Python function to calculate fibonacci numbers.",
    "What are the key differences between TCP and UDP?",
    "Describe the process of photosynthesis.",
    "How does a neural network learn?",
] * 20  # 100 prompts total

print(f"Prepared {len(benchmark_prompts)} benchmark prompts")
```

### 4. Run Benchmarks
```python
import time
import torch
from statistics import mean, stdev

def benchmark_throughput(model, tokenizer, prompts, max_new_tokens=50):
    """Measure throughput (samples/second)."""
    print("\n=== Throughput Benchmark ===")

    start_time = time.time()
    tokens_generated = 0

    for i, prompt in enumerate(prompts):
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        tokens_generated += outputs.shape[1]

        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(prompts)} prompts...")

    elapsed = time.time() - start_time
    throughput = len(prompts) / elapsed
    tokens_per_sec = tokens_generated / elapsed

    return {
        'throughput_samples_per_sec': throughput,
        'tokens_per_sec': tokens_per_sec,
        'total_time': elapsed,
        'total_samples': len(prompts)
    }

def benchmark_latency(model, tokenizer, prompts, num_runs=10):
    """Measure per-sample latency."""
    print("\n=== Latency Benchmark ===")

    latencies = []

    for i in range(num_runs):
        prompt = prompts[i % len(prompts)]
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        start = time.time()
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=50)
        latency = time.time() - start

        latencies.append(latency)
        print(f"Run {i + 1}/{num_runs}: {latency:.3f}s")

    return {
        'mean_latency': mean(latencies),
        'std_latency': stdev(latencies) if len(latencies) > 1 else 0,
        'min_latency': min(latencies),
        'max_latency': max(latencies)
    }

def benchmark_memory(model):
    """Measure memory usage."""
    print("\n=== Memory Benchmark ===")

    if torch.cuda.is_available():
        memory_allocated = torch.cuda.memory_allocated() / 1e9
        memory_reserved = torch.cuda.memory_reserved() / 1e9
        max_memory = torch.cuda.max_memory_allocated() / 1e9

        return {
            'memory_allocated_gb': memory_allocated,
            'memory_reserved_gb': memory_reserved,
            'max_memory_gb': max_memory
        }
    else:
        return {
            'memory_allocated_gb': 0,
            'memory_reserved_gb': 0,
            'max_memory_gb': 0,
            'note': 'Running on CPU'
        }

# Run all benchmarks
throughput_results = benchmark_throughput(model, tokenizer, benchmark_prompts[:50])
latency_results = benchmark_latency(model, tokenizer, benchmark_prompts, num_runs=10)
memory_results = benchmark_memory(model)
```

### 5. Generate Report
```python
import pandas as pd
import json
from datetime import datetime

# Combine all results
all_results = {
    'model_name': model_name,
    'timestamp': datetime.now().isoformat(),
    'hardware': {
        'device': str(model.device),
        'cuda_available': torch.cuda.is_available(),
        'cuda_device_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A',
    },
    'throughput': throughput_results,
    'latency': latency_results,
    'memory': memory_results
}

# Save as JSON
with open('benchmark_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

# Create CSV summary
summary_data = {
    'Metric': [
        'Throughput (samples/sec)',
        'Throughput (tokens/sec)',
        'Mean Latency (sec)',
        'Min Latency (sec)',
        'Max Latency (sec)',
        'Memory Allocated (GB)',
        'Max Memory (GB)'
    ],
    'Value': [
        f"{throughput_results['throughput_samples_per_sec']:.2f}",
        f"{throughput_results['tokens_per_sec']:.2f}",
        f"{latency_results['mean_latency']:.3f}",
        f"{latency_results['min_latency']:.3f}",
        f"{latency_results['max_latency']:.3f}",
        f"{memory_results['memory_allocated_gb']:.2f}",
        f"{memory_results['max_memory_gb']:.2f}"
    ]
}

df = pd.DataFrame(summary_data)
df.to_csv('benchmark_summary.csv', index=False)

# Print summary
print("\n" + "="*50)
print("BENCHMARK SUMMARY")
print("="*50)
print(df.to_string(index=False))
print("="*50)
print(f"\nDetailed results saved to: benchmark_results.json")
print(f"Summary saved to: benchmark_summary.csv")
```

### 6. Create Visualization (Optional)
```python
import matplotlib.pyplot as plt

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Throughput chart
axes[0].bar(['Samples/sec', 'Tokens/sec'],
            [throughput_results['throughput_samples_per_sec'],
             throughput_results['tokens_per_sec'] / 100])  # Scale for visibility
axes[0].set_title('Throughput Metrics')
axes[0].set_ylabel('Rate')

# Latency chart
latency_data = [latency_results['min_latency'],
                latency_results['mean_latency'],
                latency_results['max_latency']]
axes[1].bar(['Min', 'Mean', 'Max'], latency_data)
axes[1].set_title('Latency Distribution (seconds)')
axes[1].set_ylabel('Time (s)')

plt.tight_layout()
plt.savefig('benchmark_visualization.png', dpi=300, bbox_inches='tight')
print(f"Visualization saved to: benchmark_visualization.png")
```

## Expected Output
- `benchmark_results.json`: Complete benchmark data in JSON format
- `benchmark_summary.csv`: Summary table of key metrics
- `benchmark_visualization.png`: Charts showing performance metrics
- Console output with real-time progress and final summary

## Troubleshooting

### CUDA Out of Memory
```bash
# Reduce batch size or use CPU
export CUDA_VISIBLE_DEVICES=""
# Or use smaller model precision
# Change torch.float16 to torch.float32 if accuracy issues occur
```

### Model Download Fails
```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/large/disk
# Or use manual download
# Visit https://huggingface.co/Qwen/Qwen-3B and download manually
```

### Import Errors
```bash
# Ensure all dependencies are installed
pip install --upgrade torch transformers datasets pandas matplotlib
```

### Slow Performance on CPU
If running on CPU, expect significantly longer execution times. Consider:
- Reducing the number of benchmark samples
- Using a smaller model variant
- Running on GPU-enabled hardware

## Success Criteria
- [x] Model downloads and loads successfully
- [x] Benchmark completes all test prompts without errors
- [x] Results saved to JSON and CSV files
- [x] Throughput > 0.1 samples/sec (CPU) or > 1 sample/sec (GPU)
- [x] Latency measurements are consistent (std < mean)
- [x] Memory usage within available GPU/RAM limits

## Next Steps
- Try different batch sizes for optimal throughput
- Compare with other model sizes (Qwen-7B, Qwen-14B)
- Run on different hardware for performance comparison
- Test with domain-specific prompts relevant to your use case
- Integrate into CI/CD pipeline for regression testing

## Related Skills
- `benchmark-llama`
- `optimize-inference-performance`
- `setup-ml-environment`
- `model-quantization`

## References
- [Qwen Model Card](https://huggingface.co/Qwen/Qwen-3B)
- [HuggingFace Transformers Docs](https://huggingface.co/docs/transformers)
- [MMLU Benchmark Paper](https://arxiv.org/abs/2009.03300)
- [PyTorch Benchmarking Guide](https://pytorch.org/tutorials/recipes/recipes/benchmark.html)
