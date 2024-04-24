# getinto the webapp

```
docker-compose -p fastapi_test-xyzp run --rm --no-deps webapp /bin/bash 
```

# install jupyter, snoop

```
docker-compose -p fastapi_test-xyzp run --rm --no-deps webapp /bin/bash

# setup poetry (also checks if pyproject.toml  already exists)
poetry init (which will create )

# activate venv
poetry shell

# add packages
poetry add --dev jupyterlab

poetry add --dev snoop
```

# Setup jupter lab

NOTE: install ipykernel will install both jupter notebook and jupter lab

To add a virtual environment to Jupyter Notebook or JupyterLab, you need to install the ipykernel package in your virtual environment and then create a kernel for that environment. 

STEP1: Activate Your Virtual Environment:Activate your virtual environment using the appropriate command for your operating system. For example:
```bash
source <virtualenv_name>/bin/activate  # For Unix/Linux
<virtualenv_name>\Scripts\activate     # For Windows

poetry shell
```

STEP2: Install ipykernel:Once your virtual environment is activated, install the ipykernel package using pip:
```
poetry install ipykernel (its already installed by jupyterlab)
```

STEP3: Create the Kernel:After installing ipykernel, you need to create a kernel for your virtual environment. Use the following command:
```css
python -m ipykernel install --user --name=<kernel_name>

python -m ipykernel install --user --name=customvenv
```

Replace <kernel_name> with the name you want to give to your kernel. This name will be displayed in Jupyter Notebook or JupyterLab.
Now, when you launch Jupyter Notebook or JupyterLab from within your virtual environment, you should see the kernel you created listed among the available kernels. Selecting this kernel will allow you to use the Python interpreter from your virtual environment within Jupyter.

launch jupter lab from inside venv

```
jupyter lab
```


# also create password

`jupyter lab password`  for this to persist, mount a folder



# snoop related in python

```
%load_ext snoop
!which python
```

```
%%snoop
import os, sys
sys_path = sys.path
```


# run await directly in cells in jupyter

- https://stackoverflow.com/a/73527716/2897115

```
%autoawait asyncio
```
