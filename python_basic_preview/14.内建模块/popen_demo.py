import subprocess
import io

def system_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout)
    stream_stderr = io.TextIOWrapper(proc.stderr)

    str_stdout = str(stream_stdout.readlines())
    str_stderr = str(stream_stderr.read())

    return str_stdout, str_stderr

if __name__== "__main__":
    exec_cmd = 'pwd'
    print(system_cmd(exec_cmd))