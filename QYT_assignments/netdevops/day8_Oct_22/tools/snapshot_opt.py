MAX_DEPTH = 10  # 控制迭代深度

# 从列表清单中提取特定名字的快照
def get_snapshots_by_name(snapshots, snapname):
    for snapshot in snapshots:
        if snapshot[0] == snapname:
            return snapshot[1]

def get_vm_snapshot(vmobj, snapname=None):
    """
    获取特定VM对象的所有快照对象

    参数：
        vmobj(obj): 虚拟机对象
        snapname(str): 快照名称
    返回：
        VM的所有快照的列表
    """
    # 定义最终返回的VM的所有快照的列表
    all_snapshot_list = []

    # 找到的特定快照对象
    snapshot_obj = None

    # 迭代快照树, 获取每一级的快照对象
    def list_snapshots_recursively(snapshots, depth=1):
        # 声明nonlocal变量all_snapshot_list
        nonlocal all_snapshot_list

        # 控制递归深度
        if depth <= MAX_DEPTH:
            # 获取快照清单的每一个快照
            for snapshot in snapshots:
                # 把快照放入all_snapshot_list
                all_snapshot_list.append((snapshot.name, snapshot.snapshot))
                # 如果存在子快照列表对象
                if snapshot.childSnapshotList:
                    # 继续迭代, 获取所有的快照对象
                    list_snapshots_recursively(snapshot.childSnapshotList, depth + 1)

        return all_snapshot_list

    # 迭代循环, 找到VM下的所有快照
    snapshot_list = list_snapshots_recursively(vmobj.snapshot.rootSnapshotList)  # 迭代获取所有的快照对象

    # 如果希望找到特定名称的快照
    if snapname:
        try:
            # 获取特定名称的快照
            snapshot_obj = get_snapshots_by_name(snapshot_list, snapname)
        except AttributeError:
            pass
    # 返回元组, 0号位整个快照列表清单, 1号位特定名称的快照对象
    return snapshot_list, snapshot_obj