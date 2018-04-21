# gdb 实现原理

gdb主要功能的实现依赖于一个系统函数ptrace，通过man手册可以了解到，ptrace可以让父进程观察和控制其子进程的检查、执行，改变其寄存器和内存的内容，主要应用于打断点（也是gdb的主要功能）和打印系统调用轨迹。

## 一、ptrace函数
函数原型如下：

```c
#include <sys/ptrace.h>
long ptrace(enum __ptrace_request request, pid_t pid,
           void *addr, void *data);
```

ptrace系统调用的request主要选项

### PTRACE_TRACEME

表示本进程将被其父进程跟踪，交付给这个进程的所有信号（除SIGKILL之外），都将使其停止，父进程将通过wait()获知这一情况。

### PTRACE_ATTACH

attach到一个指定的进程，使其成为当前进程跟踪的子进程，子进程的行为等同于它进行了一次PTRACE_TRACEME操作。

### PTRACE_CONT
继续运行之前停止的子进程。可同时向子进程交付指定的信号。

更多参数请`man ptrace`

## 二、gdb使用ptrace的基本流程

gdb调试一个新进程：通过fork函数创建一个新进程，在子进程中执行ptrace(PTRACE_TRACEME, 0, 0, 0)函数，然后通过execv()调用准备调试的程序。
attach到已运行进程：将pid传递给gdb，然后执行ptrace(PTRACE_ATTACH, pid, 0, 0)。

在使用参数为PTRACE_TRACEME或PTRACE_ATTACH的ptrace系统调用建立调试关系之后，交付给目标程序的任何信号（除SIGKILL之外）都将被gdb先行截获，gdb因此有机会对信号进行相应处理，并根据信号的属性决定在继续目标程序运行时是否将之前截获的信号实际交付给目标程序。

## 三、gdb使用的内核机制

断点的功能是通过内核信号实现的，以x86为例，内核向某个地址打入断点，实际上就是往该地址写入断点指令INT 3，即0xCC。目标程序运行到这条指令之后就会触发SIGTRAP信号，gdb捕获到这个信号，根据目标程序当前停止位置查询gdb维护的断点链表，若发现在该地址确实存在断点，则可判定为断点命中。

内核是通过如下调用进入内核态的：

`SYSCALL_DEFINE4(ptrace, long, request, long, pid, long, addr, long, data)`

根据不同的request调用不同函数，基本都是判断当前进程task中ptrace选项，走security_ptrace函数，在linux security模块中，然后汇编。