+++
title = "Jupyter"
description = "Misc Setups and Configurations for Jupyter"
tags = [
    "jupyter",
    "python",
]
date = "2023-11-20"
categories = [
    "Utils",
]
menu = "main"
parent = "tutorials"
+++

### Memory Usage
```python
def memory():
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
    return ret
```

### No Hang Up 
```powershell
nohup jupyter notebook --no-browser > notebook.log 2>&1 &
```

### Workaround: no cells output
```python
se = time.time()
print(train.rdd.getNumPartitions())
print(test.rdd.getNumPartitions())
e = time.time()
print("Training time = {}".format(e - se))

your_float_variable = (e - se)
comment = "Training time for getnumpartition:"

# Open the file in append mode and write the comment and variable
with open('output.txt', 'a') as f:
    f.write(f"{comment} {your_float_variable}\n")
```


## Related Entries
- [Run plotly in JupyterLab](https://non-neutralzero.github.io/docs/posts/dash-jupyterlab/)