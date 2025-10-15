from fastapi import Depends, FastAPI, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Union
import subprocess, io, base64

def system_cmd(cmd):
    '''
    根据传入的CMD执行Linux命令

    参数：
        cmd(str): 命令
    返回：
        包含标准输出和错误信息的元组
    '''
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout)
    stream_stderr = io.TextIOWrapper(proc.stderr)

    str_stdout = str(stream_stdout.read())
    str_stderr = str(stream_stderr.read())

    return str_stdout, str_stderr


# 定义请求执行CMD的数据结构
class PostCMD(BaseModel):
    # {"cmd": "ifconfig"}
    cmd: str = Field(title='执行的命令')

# 定义返回执行CMD的结果的数据结构
class ReturnCMD(BaseModel):
    # {"cmd": "ifconfig",
    # "cmd_result": "执行的命令返回的结果，已经被Base64编码"}
    cmd: str = Field(title='执行的命令')
    cmd_result: str = Field(title='执行的命令返回的结果，已经被Base64编码')

# 定义返回错误的数据结构
class ERROR(BaseModel):
    # {"error": "错误信息"}
    error: str = Field(title='错误信息')

# 创建FastAPI实例
app = FastAPI()

# 执行系统命令
# Post的数据类型为PostCMD, 传递给变量postcmd
# 返回的数据类型为ReturnCMD
@app.post("/cmd", response_model=Union[ReturnCMD, ERROR], summary='执行系统命令', description='执行系统命令描述')
async def cmd(postcmd: PostCMD, request:Request):
    exec_cmd = postcmd.cmd
    # 使用"subprocess.Popen"执行命令
    cmd_result = system_cmd(exec_cmd)
    if cmd_result[1]:
        # 将命令执行的错误结果转换成字节对象，再用Base64进行编码转换到安全的输出
        return ERROR(error=base64.b64encode(cmd_result[1].encode()).decode())
    # 如果cmd_result[1]没有返回内容，表示命令执行成功
    else:
        # 将命令执行的结果转换成字节对象，再用Base64进行编码转换到安全的输出
        return ReturnCMD(cmd=exec_cmd, cmd_result=base64.b64encode(cmd_result[0].encode()).decode())