import json
import io
import contextlib
import os
import warnings
warnings.filterwarnings('ignore')

# First re-generate clean base notebook
os.system('python generate_notebook.py')

with open('src/analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

from IPython.core.interactiveshell import InteractiveShell

# Initialize IPython shell
shell = InteractiveShell.instance()

execution_counter = 1

for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        code = ''.join(cell['source'])
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            result = shell.run_cell(code)
            
        stdout_text = stdout_capture.getvalue()
        cell_outputs = []
        
        if stdout_text:
            cell_outputs.append({
                "name": "stdout",
                "output_type": "stream",
                "text": [line + '\n' for line in stdout_text.splitlines()]
            })
            
        if result.error_in_exec:
            err = result.error_in_exec
            cell_outputs.append({
                "ename": type(err).__name__,
                "evalue": str(err),
                "output_type": "error",
                "traceback": [str(err)]
            })
            print(f"Error in cell {execution_counter}: {err}")
        elif result.result is not None:
            res_val = result.result
            import pandas as pd
            if isinstance(res_val, (pd.DataFrame, pd.Series)):
                text_repr = res_val.to_string()
            else:
                text_repr = repr(res_val)
            cell_outputs.append({
                "data": {
                    "text/plain": [line + '\n' for line in text_repr.splitlines()]
                },
                "execution_count": execution_counter,
                "metadata": {},
                "output_type": "execute_result"
            })
            
        cell['outputs'] = cell_outputs
        cell['execution_count'] = execution_counter
        execution_counter += 1

with open('src/analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Successfully executed all {execution_counter - 1} code cells!")
