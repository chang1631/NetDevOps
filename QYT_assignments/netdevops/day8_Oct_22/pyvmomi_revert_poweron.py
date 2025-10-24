from tools import service_instance
from tools.login_info import host, username, password
from tools.snapshot_opt import get_vm_snapshot
from pyvmomi_get_vm_by_rp import get_resource_pool, get_vms_in_resource_pool
from pyVim.connect import Disconnect
from pyVmomi import vim, vmodl
import atexit

def wait_for_tasks(si, tasks):
    """
    等待一个或多个 vSphere 异步任务完成

    参数：
        si(obj):vCenter连接会话实例
        tasks(list): 任务列表
    """
    # 初始化PropertyCollector，用来监听任务状态的变化
    property_collector = si.content.propertyCollector
    # 存储任务的字符串形式，用于追踪未完成任务
    task_list = [str(task) for task in tasks]
    # 告诉 PropertyCollector 要监听哪些对象（这里是任务对象）
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks]
    # 告诉 PropertyCollector 要监听哪些属性（这里 all=True，监听任务的所有属性）
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task, pathSet=[], all=True)
    # 组合对象和属性，用来创建 PropertyCollector 过滤器
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    # 构建过滤器对象，可以订阅任务状态变化
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)

    try:
        version, state = None, None
        while task_list:
            # 进行阻塞直到有任务状态更新
            update = property_collector.WaitForUpdates(version)
            # 遍历过滤器对象
            for filter_set in update.filterSet:
                # 遍历任务对象以判断是否执行完成
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    # 遍历PropertyCollector返回更新信息
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue
                        # 任务执行成功则从未完成列表中移除。
                        if state == vim.TaskInfo.State.success:
                            task_list.remove(str(task))
                        # 任务执行失败则抛出任务的异常，脚本会终止
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # PropertyCollector需要版本号，保证每次循环只处理新更新
            version = update.version
    finally:
        # 过滤器是有资源占用的对象，用完必须销毁
        if pcfilter:
            pcfilter.Destroy()


def revert_snapshot_and_poweron(si, vmobj, snapname):
    """
    恢复虚拟机快照，并在快照恢复完成后开机

    参数：
        vmobj(obj): 虚拟机对象
        snapname: 镜像名称
    """
    # 获取特定快照
    snapshot_list, snapshot_obj = get_vm_snapshot(vmobj, snapname)
    if not snapshot_obj:
        raise ValueError(f"快照 {snapname} 不存在！")

    # 恢复快照（异步任务）
    print(f"开始恢复虚拟机 {vmobj.name} 的快照 {snapname} ...")
    revert_task = snapshot_obj.RevertToSnapshot_Task()

    # 等待任务完成
    wait_for_tasks(si, [revert_task])
    print(f"虚拟机 {vmobj.name} 快照 {snapname} 恢复完成！")

    # 开机虚拟机
    print(f"开始开机虚拟机 {vmobj.name} ...")
    poweron_task = vmobj.PowerOnVM_Task()
    wait_for_tasks(si, [poweron_task])
    print(f"虚拟机 {vmobj.name} 已开机！")

if __name__ == "__main__":
    # 初始化vCenter连接会话实例
    si = service_instance.connect(host, username, password)
    atexit.register(Disconnect, si)

    # 建立获取vSphere内容的链接
    content = si.RetrieveContent()

    # 要查找的资源池的名称
    resource_pool_name = "MyResourcePool"
    # 先找到特定名称的资源池对象
    resource_pool_obj = get_resource_pool(content, resource_pool_name)
    # 获取"MyResourcePool"资源池中所有的虚拟机
    vms = get_vms_in_resource_pool(resource_pool_obj)

    # 遍历获取的虚拟机
    for vm in vms:
        # 虚拟机的名称
        vm_name = vm.name
        # 想要获取的镜像名称
        snapshot_name = f'{vm_name}_22_Oct'
        # 恢复快照并开机
        revert_snapshot_and_poweron(si, vm, snapshot_name)
