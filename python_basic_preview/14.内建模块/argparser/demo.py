def qyt_argparse(host, filename, iface):
    print(host)
    print(filename)
    print(iface)

if __name__ == '__main__':
    from argparse import ArgumentParser

    # 使用方法的说明
    usage = "python arg_oarse.py ipaddress -f filename -i interface"
    #初始化ArgumentParser实例并传入usage说明
    parser = ArgumentParser(usage=usage)

    '''
    | 参数项               | 含义                          |
    | ----------------- | --------------------------- |
    | `-f`, `--file`    | 命令行选项名称，可以任选其一输入            |
    | `dest='filename'` | 解析后的值将保存在 `args.filename` 中 |
    | `default='1.txt'` | 如果用户不输入，默认值为 `'1.txt'`      |
    | `type=str`        | 参数值会被转换为字符串类型               |
    | `help=...`        | 参数说明，在 `--help` 时显示         |
    '''

    parser.add_argument("-f","--file",dest="filename",help="Write content to FILE",default='1.txt',type=str)
    parser.add_argument("-i","--interface",dest="iface",help="Specify an interface",default=1,type=int)
    # parser.add_argument(nargs='?',dest="host",help="Specify an host",default='10.1.1.1',type=str)
    parser.add_argument(nargs='*', dest="hosts",help="Specify an host",default='10.1.1.1 10.1.1.2',type=str)

    #解析传入的参数
    args = parser.parse_args()

    qyt_argparse(args.hosts, args.filename, args.iface)