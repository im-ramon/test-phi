### How to start the project
1. Download the Phi-3 model
```shel
huggingface-cli download microsoft/Phi-3-mini-128k-instruct-onnx --include cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/* --local-dir .
```
2. Active virtual environment
```shel
python -m venv venv ; .\venv\Scripts\activate
```

3. Install Python dependencies
```shel
pip install -r "requirements.txt"
```

3. Run
```shell
python app.py 
```