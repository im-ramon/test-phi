### How to start the project
1. Download the Phi-3 model
```shel
huggingface-cli download microsoft/Phi-3-mini-128k-instruct-onnx --include cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/* --local-dir .
```
2. Install Python requirements
```shel
pip install -r "requirements.txt"
```

3. Start
```shell
.\venv\Scripts\activate ; python app.py 
```