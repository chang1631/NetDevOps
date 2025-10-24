```python
Written by Michael Rice <michael@michaelrice.org>

Github: https://github.com/michaelrice
Website: https://michaelrice.github.io/
Blog: http://www.errr-online.com/
This code has been released under the terms of the Apache 2 licenses
http://www.apache.org/licenses/LICENSE-2.0.html

Helper module for task operations.
"""
from pyVmomi import vim
from pyVmomi import vmodl


def wait_for_tasks(si, tasks):
    """Given the service instance and tasks, it returns after all the
   tasks are complete
   """
    property_collector = si.content.propertyCollector
    task_list = [str(task) for task in tasks]
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while task_list:
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()
```

好的，这段代码是一个典型的 **PyVmomi（Python 操作 VMware vSphere API）辅助函数**，用于 **等待一个或多个 vSphere 异步任务完成**。我给你分步骤详细解释每一部分。

---

## 🧩 1️⃣ 导入模块

```python
from pyVmomi import vim
from pyVmomi import vmodl
```

* `vim`：vSphere API 的核心对象模型（VM、Datastore、Task、Host 等）。
* `vmodl`：vSphere API 的底层模块，用于处理查询、异常等底层对象。

---

## 🧩 2️⃣ 函数定义

```python
def wait_for_tasks(si, tasks):
    """Given the service instance and tasks, it returns after all the tasks are complete"""
```

* `si`：vCenter / ESXi 的 ServiceInstance 对象（通过 `SmartConnect` 获取）。
* `tasks`：一个或多个 `vim.Task` 对象列表，通常是异步操作返回的任务，如：

  * VM 创建
  * 虚拟机开关机
  * 快照操作
* 函数目的是 **阻塞当前脚本，直到所有任务完成（成功或失败）**。

---

## 🧩 3️⃣ 准备 PropertyCollector

```python
property_collector = si.content.propertyCollector
task_list = [str(task) for task in tasks]
```

* vSphere 的 **任务是异步的**，执行任务时不会立即返回结果。
* **PropertyCollector** 是 vSphere 的核心机制，用来 **监听对象状态变化**（比如任务状态）。
* `task_list`：存储任务的字符串形式，用于追踪未完成任务。

---

## 🧩 4️⃣ 创建过滤器

```python
obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
             for task in tasks]
property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                           pathSet=[],
                                                           all=True)
filter_spec = vmodl.query.PropertyCollector.FilterSpec()
filter_spec.objectSet = obj_specs
filter_spec.propSet = [property_spec]
pcfilter = property_collector.CreateFilter(filter_spec, True)
```

* `ObjectSpec`：告诉 PropertyCollector **要监听哪些对象**（这里是任务对象）。
* `PropertySpec`：告诉 PropertyCollector **要监听哪些属性**（这里 `all=True`，监听任务的所有属性）。
* `FilterSpec`：组合对象和属性，用来创建 PropertyCollector **过滤器**。
* `pcfilter`：真正的过滤器对象，可以 **订阅任务状态变化**。

> 💡 作用：只有通过 PropertyCollector 创建过滤器，才能高效监听任务状态，而不是轮询。

---

## 🧩 5️⃣ 等待任务完成

```python
version, state = None, None
while task_list:
    update = property_collector.WaitForUpdates(version)
```

* `WaitForUpdates(version)` 会阻塞，直到 **有任务状态更新**。
* `version` 用于标记上一次读取的更新版本，下次只接收新变化。

---

### 解析更新循环

```python
for filter_set in update.filterSet:
    for obj_set in filter_set.objectSet:
        task = obj_set.obj
        for change in obj_set.changeSet:
            if change.name == 'info':
                state = change.val.state
            elif change.name == 'info.state':
                state = change.val
            else:
                continue
```

* vSphere 的 PropertyCollector 返回更新信息（changeSet）。
* 每个任务状态会更新 `info.state`，可能是：

  * `vim.TaskInfo.State.success` → 成功
  * `vim.TaskInfo.State.error` → 失败
  * `vim.TaskInfo.State.running` → 运行中
* 这里判断任务是否完成。

---

### 成功或失败处理

```python
if state == vim.TaskInfo.State.success:
    task_list.remove(str(task))
elif state == vim.TaskInfo.State.error:
    raise task.info.error
```

* 成功 → 从未完成列表中移除。
* 失败 → 抛出任务的异常，脚本会终止。

---

### 更新版本号

```python
version = update.version
```

* PropertyCollector 需要 **版本号**，保证每次循环只处理新更新。

---

## 🧩 6️⃣ 最后清理过滤器

```python
finally:
    if pcfilter:
        pcfilter.Destroy()
```

* PropertyCollector 的过滤器是**有资源占用的对象**，用完必须销毁。
* 放在 `finally` 中确保 **即使异常也能释放资源**。

---

## ✅ 总结

这段函数的作用就是：

> **阻塞等待一个或多个 vSphere 异步任务完成，并在任务失败时抛出异常，任务完成后自动释放资源。**

典型使用场景：

```python
# 假设 vm 是一个虚拟机对象
task = vm.PowerOnVM_Task()    # 异步任务
wait_for_tasks(si, [task])    # 等待任务完成
```

这样脚本就可以**安全依赖任务完成**再继续后续操作。

---

如果你想，我可以帮你画一张 **PropertyCollector + Task 状态更新的流程图**，让你直观理解这个循环的工作原理。

你希望我画吗？
