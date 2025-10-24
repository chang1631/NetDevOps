from pyVmomi import vim

def get_vms_in_resource_pool(resource_pool):
    """
    查找资源池下的虚拟机

    参数：
        resource_pool(obj): 资源池对象
    返回：
        虚拟机对象的列表
    """
    # 定义列表用于存储最终返回的资源池下虚拟机对象
    vms_in_group = []
    # 使用栈来存储资源池对象
    stack = [resource_pool]

    while stack:
        # 当栈不为空时, 弹出栈顶的资源池对象
        current = stack.pop()
        if current.vm:
            # 如果资源池下有虚拟机，就添加到列表中
            vms_in_group.extend(current.vm)

        # 如果资源池下有子资源池，就添加到栈中
        stack.extend(current.resourcePool)

    return vms_in_group


def get_resource_pool(content, rp_name):
    """
    从vCenter中获取指定的资源池

    参数:
        content(obj): vSphere内容的链接
        rp_name(str): 要获取的资源池名称
    返回：
        资源池对象
    """
    # 定义起始查找位置（从根文件夹开始）
    container = content.rootFolder
    # 定义要查找的对象类型（资源池）
    viewType = [vim.ResourcePool]
    # 是否递归查找
    recursive = True

    # 创建查询的View, 查询vSphere环境下所有的资源池
    containerView = content.viewManager.CreateContainerView(
        container, viewType, recursive)

    # 遍历资源池对象
    for rp in containerView.view:
        # 如果资源池名称与查询的资源池名称相同，就返回这个资源池对象
        if rp.name == rp_name:
            return rp

    return None