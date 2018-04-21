

# execve系统调用

execve系统调用完成的功能是，把当前进程代码替换为新的二进制代码，并执行。调用execve系统调用的进程如果已经被调试（PF_PTRACED置位），则把代码转入后则会向自身发送信号SIGTRAP，使其中止执行。这样可以使调试器装入代码后，进程停止在代码的最开始。
对于不同的二进制文件，execve调用不同的代码。以下是aout和elf文件格式的代码转入程序中完成上述功能的代码。
```c
do_load_elf_binary()函数（/linux/fs/binfmt_elf.c）
    ...
    if (current->flags & PF_PTRACED)
    send_sig(SIGTRAP, current, 0);
    ...

do_load_aout_binary()函数（/linux/fs/binfmt_aout.c）
    ...
    if (current->flags & PF_PTRACED)
        send_sig(SIGTRAP, current, 0);
    ...
```

