# Benchmark Testing System

This directory contains a comprehensive benchmark testing system for evaluating different LLM models and configurations on Salesforce AIOps tasks.

## 🚀 Quick Start

### List Available Configurations
```bash
python list_configs.py
```

### Run Single Configuration
```bash
# Run specific model configuration
./benchmark.sh salesforce_gpt5
./benchmark.sh salesforce_claude4_transform

# Run with custom options
./benchmark.sh salesforce_gemini25_pro --quiet
./benchmark.sh salesforce_gpt5_mini --no-report
```

### Run Batch Tests
```bash
# Run all model configurations (transform=false)
./benchmark.sh --all-models

# Run all transform configurations (transform=true)  
./benchmark.sh --all-transform

# Run ALL configurations
./benchmark.sh --all

# Run with minimal output
./benchmark.sh --all --quiet
```

## 📋 Available Configurations

### LLM Models Tested
- **GPT-5** (`openai` type)
- **GPT-5-Mini** (`openai` type)
- **Claude-4** (`claude` type)
- **Claude-3.7** (`claude` type)
- **Gemini-2.5-Pro** (`gemini_vertex` type)
- **Gemini-2.5-Flash** (`gemini_vertex` type)

### Configuration Variants
Each model has two variants:
1. **Standard**: `transform_tool_response_by_coding = false`
2. **Transform**: `transform_tool_response_by_coding = true`

### Configuration Files
```
mcpuniverse/benchmark/configs/test/
├── salesforce.yaml                           # Original Gemini-2.5-Pro
├── salesforce_no_trans.yaml                  # Original GPT-5
├── salesforce_gpt5.yaml                      # GPT-5 (no transform)
├── salesforce_gpt5_transform.yaml            # GPT-5 (with transform)
├── salesforce_gpt5_mini.yaml                 # GPT-5-Mini (no transform)
├── salesforce_gpt5_mini_transform.yaml       # GPT-5-Mini (with transform)
├── salesforce_claude4.yaml                   # Claude-4 (no transform)
├── salesforce_claude4_transform.yaml         # Claude-4 (with transform)
├── salesforce_claude37.yaml                  # Claude-3.7 (no transform)
├── salesforce_claude37_transform.yaml        # Claude-3.7 (with transform)
├── salesforce_gemini25_pro.yaml              # Gemini-2.5-Pro (no transform)
├── salesforce_gemini25_pro_transform.yaml    # Gemini-2.5-Pro (with transform)
├── salesforce_gemini25_flash.yaml            # Gemini-2.5-Flash (no transform)
└── salesforce_gemini25_flash_transform.yaml  # Gemini-2.5-Flash (with transform)
```

## 🛠️ Scripts

### `run_benchmark.py`
Main Python script for running individual benchmarks.

**Usage:**
```bash
python run_benchmark.py --config test/salesforce_gpt5.yaml
python run_benchmark.py --config test/salesforce_claude4.yaml --quiet
python run_benchmark.py --config test/salesforce_gemini25_pro.yaml --no-report
```

**Options:**
- `--config, -c`: Path to benchmark configuration YAML file (required)
- `--log-file, -l`: Custom log file path (optional, auto-generated if not specified)
- `--no-report`: Skip generating benchmark report
- `--quiet, -q`: Suppress verbose output
- `--output-dir, -o`: Directory for output files (default: log)

### `benchmark.sh`
Bash wrapper script for convenient benchmark execution and batch processing.

**Single Configuration:**
```bash
./benchmark.sh salesforce_gpt5                    # Run specific config
./benchmark.sh salesforce_claude4_transform       # Run transform variant
./benchmark.sh test/custom.yaml                   # Run custom config file
```

**Batch Processing:**
```bash
./benchmark.sh --all                              # Run ALL configurations
./benchmark.sh --all-models                       # Run all model configs (no transform)
./benchmark.sh --all-transform                    # Run all transform configs
```

**Additional Options:**
```bash
./benchmark.sh --all --quiet                      # Batch run with minimal output
./benchmark.sh salesforce_gpt5 --no-report        # Single run without report
```

### `list_configs.py`
Utility script to display all available configurations with their details.

```bash
python list_configs.py
```

## 📊 Output and Results

### Log Files
- Default location: `log/` directory
- Naming convention: `<config_name>_benchmark.log`
- Example: `log/salesforce_gpt5_benchmark.log`

### Benchmark Reports
- Generated automatically unless `--no-report` is specified
- Contains detailed evaluation results and metrics
- Saved alongside log files

### Batch Execution Summary
When running batch tests, you'll get:
- Individual test results with ✅/❌ indicators
- Summary statistics (total, successful, failed)
- List of failed configurations for debugging

## 🔧 Configuration Structure

Each YAML configuration contains three sections:

### 1. LLM Configuration
```yaml
kind: llm
spec:
  name: llm-1
  type: openai  # or claude, gemini_vertex
  config:
    model_name: gpt-5
```

### 2. Agent Configuration
```yaml
kind: agent
spec:
  name: ReAct-agent
  type: react
  config:
    llm: llm-1
    instruction: You are an agent expert at various AIOps related tasks at Salesforce.
    max_iterations: 40
    transform_tool_response_by_coding: false  # or true
    servers:
      - name: salesforce-falcon-metadata
      - name: salesforce-gus
      # ... other servers
```

### 3. Benchmark Configuration
```yaml
kind: benchmark
spec:
  description: Test agent for salesforce tasks with GPT-5.
  agent: ReAct-agent
  tasks:
    - test/salesforce/task1_simple_example.json
    - test/salesforce/task2_simple_example.json
    # ... other tasks
```

## 🎯 Use Cases

### Development Testing
```bash
# Test a specific model during development
./benchmark.sh salesforce_gpt5 --quiet
```

### Model Comparison
```bash
# Compare all models without transform
./benchmark.sh --all-models

# Compare transform vs no-transform for specific model
./benchmark.sh salesforce_claude4
./benchmark.sh salesforce_claude4_transform
```

### CI/CD Integration
```bash
# Run all tests in automated pipeline
./benchmark.sh --all --quiet --no-report --output-dir results/
```

### Performance Analysis
```bash
# Run comprehensive test suite
./benchmark.sh --all

# Analyze results in log/ directory
ls -la log/salesforce_*_benchmark.log
```

## 📈 Evaluation Metrics

Each benchmark evaluates:
- Task completion success rate
- Individual evaluation function results
- Pass/fail status for each test case
- Execution time and performance metrics

## 🔍 Troubleshooting

### Common Issues
1. **Configuration not found**: Check file path and ensure YAML files exist
2. **LLM authentication**: Ensure API keys are properly configured
3. **Server connectivity**: Verify MCP servers are accessible
4. **Memory issues**: Use `--quiet` flag for large batch runs

### Debug Mode
```bash
# Run with verbose output for debugging
./benchmark.sh salesforce_gpt5  # (without --quiet)

# Check specific log file
tail -f log/salesforce_gpt5_benchmark.log
```

## 🚀 Adding New Configurations

To add a new LLM model or configuration:

1. Create new YAML file in `mcpuniverse/benchmark/configs/test/`
2. Follow the naming convention: `salesforce_<model>_<variant>.yaml`
3. Update the LLM type and model name in the configuration
4. Test with: `./benchmark.sh your_new_config`

Example for adding GPT-6:
```yaml
kind: llm
spec:
  name: llm-1
  type: openai
  config:
    model_name: gpt-6
```

The batch processing scripts will automatically detect and include new configurations!
