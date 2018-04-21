# elf文件格式
------
目录
--

> * elf文件的分类
> * 可重定位的对象文件
> * 可被共享的对象文件
> * 可执行的对象文件 
> * elf文件的组成
  ELF头部、程序头部表、节区或段、节区头部表
> * ELF文件头

## elf文件的分类
* 可重定位的对象文件(Relocatable file)

        这是由汇编器汇编生成的 .o 文件。后面的链接器拿它作为输入，经链接处理后，生成一个可执行的对象文件 (Executable file) 或者一个可被共享的对象文件(Shared object file)

* 可执行的对象文件(Executable file)

        很常见，如文本编辑器vi等等。可执行的脚本(如shell脚本)不是 Executable object file，它们只是文本文件，一般无扩展名。

* 可被共享的对象文件(Shared object file)

        这就是所谓的动态库文件，也即 .so 文件。动态库在发挥作用的过程中，必须经过两个步骤：
        （1） 链接编辑器拿它和其他Relocatable object file以及shared object file作为输入，经链接处理后，生存另外的 shared object file 或者 executable file。
        （2)  在运行时，动态链接器(dynamic linker)拿它和一个Executable file以及另外一些 Shared object file 来一起处理，在Linux系统里面创建一个进程映像。
* 核心转储文件(Core dump file)

        当进程意外终止时，系统可以将，该进程的地址空间内容及终止时的一些其他信息转储到核心转储文件，比如linux下的core dump
## elf文件的组成
elf文件大都包含ELF头部、程序头部表、节区或段、节区头部表。 ELF 头部用来描述整个文件的组织。节区部分包含链接视图的指令、数据、符号表、重定位信息等。程序头部表告诉系统如何创建进程映像。节区头部表包含了描述文件节区的信息，如名称、大小。

![cmd-markdown-logo](https://img-blog.csdn.net/20160521110158483)

 - 组成不同的可重定位文件（.o 文件）参与可执行文件或者可被共享的对象文件的链接构建。不需要程序头部表。必须包含节区头部表。以节为单位。
 - 组成可执行文件或者可被共享的对象文件（.so文件）在运行时内存中进程映像的构建。 必须具有程序头部表。可以无节区头部表。以段为单位。
| 可重定位文件 | 可执行或可被共享的对象文件 |
| -----  | -------  | 
| ELF头部     | ELF头部 |
| 程序头部表（可无）        |   程序头部表（必须）   |
| 很多节区        |    很多段    |
| 节区头部表（必须）        |    节区头部表（可无）    |

## 文件头
首先，写一段C程序代码

```C
#include<stdio.h>

int addTwoIntegers(int firstInFunction, int secondInFunction){
	return firstInFunction + secondInFunction;
}

int main(void){
	int firstInteger, secondInteger, sumInteger;
	firstInteger = 2;
	secondInteger = 3;
	sumInteger = addTwoIntegers(firstInteger, secondInteger);
	printf("sum is %d", sumInteger);
	return 0;
} 
```

使用

```
     readelf -h ./a.out
```

命令可以读取elf文件（编译生成的 a.out）的文件头，内容如下

    ELF 头：
      Magic：   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
      类别:                              ELF64
      数据:                              2 补码，小端序 (little endian)
      版本:                              1 (current)
      OS/ABI:                            UNIX - System V
      ABI 版本:                          0
      类型:                              EXEC (可执行文件)
      系统架构:                          Advanced Micro Devices X86-64
      版本:                              0x1
      入口点地址：               0x400430
      程序头起点：          64 (bytes into file)
      Start of section headers:          6656 (bytes into file)
      标志：             0x0
      本头的大小：       64 (字节)
      程序头大小：       56 (字节)
      Number of program headers:         9
      节头大小：         64 (字节)
      节头数量：         31
      字符串表索引节头： 28

* 入口点地址
是指程序第一条要运行的指令的运行时地址，如这个a.out的进入点是 0x400430。可重定位文件只是供再链接，不会有程序进入点（这里会是0），而可执行文件和动态库都存在进入点。可执行文件的进入点指向C库中的_start，动态库中的进入点指向 call_gmon_start。
* Number of program headers、Number of section headers
指程序头部表和段表的数量。可重定位文件必须有节区头部表（有section），可执行文件或可共享文件必须有程序头部表（有segments），本头的大小(size of this header)指这个ELF文件头本身的大小，程序头大小指程序头部表的大小，特别地其中字符串索引节头表示字符串表中ELF文件头的字符串所在表中的索引。
* 魔数
最前面Magic的十六个字节被规定用来标识ELF文件的，操作系统通过这16个字节来达成识别ELF文件的目的，7f对应ASCII码中DEL控制符，随后三个字节分别表示‘E’，‘L’，‘F’对应的ASCII码，之后第五个字节02表示是64位的，第六个字节表示字节序01表示小端序，第七个字节表示ELF文件的主版本号，大多数均为01，这是因为ELF标准自1.2后已经不更新了，后9位ELF标准没有特殊规定，但一些平台上被用作扩展标记，在加载前会先确认魔数是否正确，如果不正确会拒绝加载。
* 其中start of section header和start of program header表示段和程序起始地址

## 节区头部表
使用
```
readelf -S ./a.out
```

命令可以读取elf文件（编译生成的 a.out）的节区头部表 section head table，内容如下
共有 31 个节头，从偏移量 0x1a00 开始：

    （摘取了部分）
    节头：
      [号] 名称              类型             地址              偏移量
           大小              全体大小          旗标   链接   信息   对齐
      [ 0]                   NULL             0000000000000000  00000000
           0000000000000000  0000000000000000           0     0     0
      [ 5] .dynsym           DYNSYM           00000000004002b8  000002b8
           0000000000000060  0000000000000018   A       6     1     8
      [ 6] .dynstr           STRTAB           0000000000400318  00000318
           000000000000003f  0000000000000000   A       0     0     1
      [23] .got              PROGBITS         0000000000600ff8  00000ff8
           0000000000000008  0000000000000008  WA       0     0     8
      [24] .got.plt          PROGBITS         0000000000601000  00001000
           0000000000000028  0000000000000008  WA       0     0     8
      [25] .data             PROGBITS         0000000000601028  00001028
           0000000000000010  0000000000000000  WA       0     0     8
      [26] .bss              NOBITS           0000000000601038  00001038
           0000000000000008  0000000000000000  WA       0     0     1
      [27] .comment          PROGBITS         0000000000000000  00001038
           0000000000000034  0000000000000001  MS       0     0     1
      [28] .shstrtab         STRTAB           0000000000000000  000018f4
           000000000000010c  0000000000000000           0     0     1
      [29] .symtab           SYMTAB           0000000000000000  00001070
           0000000000000660  0000000000000018          30    47     8
      [30] .strtab           STRTAB           0000000000000000  000016d0
           0000000000000224  0000000000000000           0     0     1
    

 - 偏移量
 是该section离开文件头部位置的距离

 - 大小
 表示section的字节大小

 - 全体大小：
	只对某些形式的sections 有意义（如符号表 .symtab section），其内部包含了一个表格，这个字段表示表格的每一个条目的特定长度

 - 旗标
 Key to Flags:
      W (write), A (alloc), X (execute), M (merge), S (strings), l (large)
      I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
      O (extra OS processing required) o (OS specific), p (processor specific)

 - 一些section

	* .text section 
	里面存储的是代码，是可执行的 (旗标为 X)
	* .data section
	里面存放的都是可写的(W)数据(非在堆栈中定义的数据),储存初始化过的数据如定义的赋过初值的全局变量等；
	* .bss section
	存放的数据可写(W)，是未经过初始化的数据。当可执行程序被执行的时候，动态链接器会在内存中开辟一定大小的空间来存放这些未初始化的数据，里面的内存单元都被初始化成0。可执行程序文件中记录有在程序运行时，需要开辟多大的空间来容纳这些未初始化的数据。
    * .symtab和.strtab section
		没有标志A，即 non-Allocable 的 sections，它们只是被链接器、调试器或者其他类似工具所使用的，而并非参与进程的运行。当运行最后的可执行程序时，加载器会加载那些 Allocable 的部分，而 non-Allocable 的部分则会被继续留在可执行文件内。因此这些 non-Allocable 的 section 都可以从最后的可执行文件中删除掉，而照样能够运行，但不可以做调试之类的事情。这两个 section 后面会说明

## .text section
使用
```
objdump -d -j .text ./a.out
```

命令可以读取elf文件（编译生成的 a.out）的.text section，内容如下
```assembly
0000000000400430 <_start>:
      400430:	31 ed                	xor    %ebp,%ebp
      400432:	49 89 d1             	mov    %rdx,%r9
      400435:	5e                   	pop    %rsi
      400436:	48 89 e2             	mov    %rsp,%rdx
      400439:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
      40043d:	50                   	push   %rax
      40043e:	54                   	push   %rsp
      40043f:	49 c7 c0 f0 05 40 00 	mov    $0x4005f0,%r8
      400446:	48 c7 c1 80 05 40 00 	mov    $0x400580,%rcx
      40044d:	48 c7 c7 3a 05 40 00 	mov    $0x40053a,%rdi
      400454:	e8 b7 ff ff ff       	callq  400410 <__libc_start_main@plt>
      400459:	f4                   	hlt    
      40045a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    
    0000000000400460 <deregister_tm_clones>:
      400460:	b8 3f 10 60 00       	mov    $0x60103f,%eax
      400465:	55                   	push   %rbp
      400466:	48 2d 38 10 60 00    	sub    $0x601038,%rax
      40046c:	48 83 f8 0e          	cmp    $0xe,%rax
      400470:	48 89 e5             	mov    %rsp,%rbp
      400473:	76 1b                	jbe    400490 <deregister_tm_clones+0x30>
      400475:	b8 00 00 00 00       	mov    $0x0,%eax
      40047a:	48 85 c0             	test   %rax,%rax
      40047d:	74 11                	je     400490 <deregister_tm_clones+0x30>
      40047f:	5d                   	pop    %rbp
      400480:	bf 38 10 60 00       	mov    $0x601038,%edi
      400485:	ff e0                	jmpq   *%rax
      400487:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
      40048e:	00 00 
      400490:	5d                   	pop    %rbp
      400491:	c3                   	retq   
      400492:	0f 1f 40 00          	nopl   0x0(%rax)
      400496:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
      40049d:	00 00 00 
    
    00000000004004a0 <register_tm_clones>:
      4004a0:	be 38 10 60 00       	mov    $0x601038,%esi
      4004a5:	55                   	push   %rbp
      4004a6:	48 81 ee 38 10 60 00 	sub    $0x601038,%rsi
      4004ad:	48 c1 fe 03          	sar    $0x3,%rsi
      4004b1:	48 89 e5             	mov    %rsp,%rbp
      4004b4:	48 89 f0             	mov    %rsi,%rax
      4004b7:	48 c1 e8 3f          	shr    $0x3f,%rax
      4004bb:	48 01 c6             	add    %rax,%rsi
      4004be:	48 d1 fe             	sar    %rsi
      4004c1:	74 15                	je     4004d8 <register_tm_clones+0x38>
      4004c3:	b8 00 00 00 00       	mov    $0x0,%eax
      4004c8:	48 85 c0             	test   %rax,%rax
      4004cb:	74 0b                	je     4004d8 <register_tm_clones+0x38>
      4004cd:	5d                   	pop    %rbp
      4004ce:	bf 38 10 60 00       	mov    $0x601038,%edi
      4004d3:	ff e0                	jmpq   *%rax
      4004d5:	0f 1f 00             	nopl   (%rax)
      4004d8:	5d                   	pop    %rbp
      4004d9:	c3                   	retq   
      4004da:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    
    00000000004004e0 <__do_global_dtors_aux>:
      4004e0:	80 3d 51 0b 20 00 00 	cmpb   $0x0,0x200b51(%rip)        # 601038 <__TMC_END__>
      4004e7:	75 11                	jne    4004fa <__do_global_dtors_aux+0x1a>
      4004e9:	55                   	push   %rbp
      4004ea:	48 89 e5             	mov    %rsp,%rbp
      4004ed:	e8 6e ff ff ff       	callq  400460 <deregister_tm_clones>
      4004f2:	5d                   	pop    %rbp
      4004f3:	c6 05 3e 0b 20 00 01 	movb   $0x1,0x200b3e(%rip)        # 601038 <__TMC_END__>
      4004fa:	f3 c3                	repz retq 
      4004fc:	0f 1f 40 00          	nopl   0x0(%rax)
    
    0000000000400500 <frame_dummy>:
      400500:	bf 20 0e 60 00       	mov    $0x600e20,%edi
      400505:	48 83 3f 00          	cmpq   $0x0,(%rdi)
      400509:	75 05                	jne    400510 <frame_dummy+0x10>
      40050b:	eb 93                	jmp    4004a0 <register_tm_clones>
      40050d:	0f 1f 00             	nopl   (%rax)
      400510:	b8 00 00 00 00       	mov    $0x0,%eax
      400515:	48 85 c0             	test   %rax,%rax
      400518:	74 f1                	je     40050b <frame_dummy+0xb>
      40051a:	55                   	push   %rbp
      40051b:	48 89 e5             	mov    %rsp,%rbp
      40051e:	ff d0                	callq  *%rax
      400520:	5d                   	pop    %rbp
      400521:	e9 7a ff ff ff       	jmpq   4004a0 <register_tm_clones>
    
    0000000000400526 <addTwoIntegers>:
      400526:	55                   	push   %rbp
      400527:	48 89 e5             	mov    %rsp,%rbp
      40052a:	89 7d fc             	mov    %edi,-0x4(%rbp)
      40052d:	89 75 f8             	mov    %esi,-0x8(%rbp)
      400530:	8b 55 fc             	mov    -0x4(%rbp),%edx
      400533:	8b 45 f8             	mov    -0x8(%rbp),%eax
      400536:	01 d0                	add    %edx,%eax
      400538:	5d                   	pop    %rbp
      400539:	c3                   	retq   
    
    000000000040053a <main>:
      40053a:	55                   	push   %rbp
      40053b:	48 89 e5             	mov    %rsp,%rbp
      40053e:	48 83 ec 10          	sub    $0x10,%rsp
      400542:	c7 45 f4 02 00 00 00 	movl   $0x2,-0xc(%rbp)
      400549:	c7 45 f8 03 00 00 00 	movl   $0x3,-0x8(%rbp)
      400550:	8b 55 f8             	mov    -0x8(%rbp),%edx
      400553:	8b 45 f4             	mov    -0xc(%rbp),%eax
      400556:	89 d6                	mov    %edx,%esi
      400558:	89 c7                	mov    %eax,%edi
      40055a:	e8 c7 ff ff ff       	callq  400526 <addTwoIntegers>
      40055f:	89 45 fc             	mov    %eax,-0x4(%rbp)
      400562:	8b 45 fc             	mov    -0x4(%rbp),%eax
      400565:	89 c6                	mov    %eax,%esi
      400567:	bf 04 06 40 00       	mov    $0x400604,%edi
      40056c:	b8 00 00 00 00       	mov    $0x0,%eax
      400571:	e8 8a fe ff ff       	callq  400400 <printf@plt>
      400576:	b8 00 00 00 00       	mov    $0x0,%eax
      40057b:	c9                   	leaveq 
      40057c:	c3                   	retq   
      40057d:	0f 1f 00             	nopl   (%rax)
    
    0000000000400580 <__libc_csu_init>:
      400580:	41 57                	push   %r15
      400582:	41 56                	push   %r14
      400584:	41 89 ff             	mov    %edi,%r15d
      400587:	41 55                	push   %r13
      400589:	41 54                	push   %r12
      40058b:	4c 8d 25 7e 08 20 00 	lea    0x20087e(%rip),%r12        # 600e10 <__frame_dummy_init_array_entry>
      400592:	55                   	push   %rbp
      400593:	48 8d 2d 7e 08 20 00 	lea    0x20087e(%rip),%rbp        # 600e18 <__init_array_end>
      40059a:	53                   	push   %rbx
      40059b:	49 89 f6             	mov    %rsi,%r14
      40059e:	49 89 d5             	mov    %rdx,%r13
      4005a1:	4c 29 e5             	sub    %r12,%rbp
      4005a4:	48 83 ec 08          	sub    $0x8,%rsp
      4005a8:	48 c1 fd 03          	sar    $0x3,%rbp
      4005ac:	e8 17 fe ff ff       	callq  4003c8 <_init>
      4005b1:	48 85 ed             	test   %rbp,%rbp
      4005b4:	74 20                	je     4005d6 <__libc_csu_init+0x56>
      4005b6:	31 db                	xor    %ebx,%ebx
      4005b8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
      4005bf:	00 
      4005c0:	4c 89 ea             	mov    %r13,%rdx
      4005c3:	4c 89 f6             	mov    %r14,%rsi
      4005c6:	44 89 ff             	mov    %r15d,%edi
      4005c9:	41 ff 14 dc          	callq  *(%r12,%rbx,8)
      4005cd:	48 83 c3 01          	add    $0x1,%rbx
      4005d1:	48 39 eb             	cmp    %rbp,%rbx
      4005d4:	75 ea                	jne    4005c0 <__libc_csu_init+0x40>
      4005d6:	48 83 c4 08          	add    $0x8,%rsp
      4005da:	5b                   	pop    %rbx
      4005db:	5d                   	pop    %rbp
      4005dc:	41 5c                	pop    %r12
      4005de:	41 5d                	pop    %r13
      4005e0:	41 5e                	pop    %r14
      4005e2:	41 5f                	pop    %r15
      4005e4:	c3                   	retq   
      4005e5:	90                   	nop
      4005e6:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
      4005ed:	00 00 00 
    
    00000000004005f0 <__libc_csu_fini>:
      4005f0:	f3 c3                	repz retq 

```
指令对.text section 内容进行反汇编，也就是由机器码出发以x86汇编的形式显示具体内容，可以看到函数名 addTwoIntegers，该位置的汇编指令为 callq  400526

## .data section
使用
```
objdump -d -j .data  ./a.out
```

命令可以读取elf文件（编译生成的 a.out）的.data section，内容如下
```assembly
Disassembly of section .data:

0000000000601028 <__data_start>:
	...

0000000000601030 <__dso_handle>:
	...
```
可以看到没有什么数据

##  .strtab section
使用
```
readelf -x 30 ./a.out
```

命令可以读取elf文件的.strtab section，其中30是 .strtab section 在SHT表格中的索引值（在前面能看到）。内容如下

      0x00000000 00637274 73747566 662e6300 5f5f4a43 .crtstuff.c.__JC
      0x00000010 525f4c49 53545f5f 00646572 65676973 R_LIST__.deregis
      0x00000020 7465725f 746d5f63 6c6f6e65 73005f5f ter_tm_clones.__
      0x00000030 646f5f67 6c6f6261 6c5f6474 6f72735f do_global_dtors_
      0x00000040 61757800 636f6d70 6c657465 642e3735 aux.completed.75
      0x00000050 3835005f 5f646f5f 676c6f62 616c5f64 85.__do_global_d
      0x00000060 746f7273 5f617578 5f66696e 695f6172 tors_aux_fini_ar
      0x00000070 7261795f 656e7472 79006672 616d655f ray_entry.frame_
      0x00000080 64756d6d 79005f5f 6672616d 655f6475 dummy.__frame_du
      0x00000090 6d6d795f 696e6974 5f617272 61795f65 mmy_init_array_e
      0x000000a0 6e747279 00436164 642e6300 5f5f4652 ntry.Cadd.c.__FR
      0x000000b0 414d455f 454e445f 5f005f5f 4a43525f AME_END__.__JCR_
      0x000000c0 454e445f 5f005f5f 696e6974 5f617272 END__.__init_arr
      0x000000d0 61795f65 6e64005f 44594e41 4d494300 ay_end._DYNAMIC.
      0x000000e0 5f5f696e 69745f61 72726179 5f737461 __init_array_sta
      0x000000f0 7274005f 5f474e55 5f45485f 4652414d rt.__GNU_EH_FRAM
      0x00000100 455f4844 52005f47 4c4f4241 4c5f4f46 E_HDR._GLOBAL_OF
      0x00000110 46534554 5f544142 4c455f00 5f5f6c69 FSET_TABLE_.__li
      0x00000120 62635f63 73755f66 696e6900 5f49544d bc_csu_fini._ITM
      0x00000130 5f646572 65676973 74657254 4d436c6f _deregisterTMClo
      0x00000140 6e655461 626c6500 5f656461 74610070 neTable._edata.p
      0x00000150 72696e74 66404047 4c494243 5f322e32 rintf@@GLIBC_2.2
      0x00000160 2e350061 64645477 6f496e74 65676572 .5.addTwoInteger
      0x00000170 73005f5f 6c696263 5f737461 72745f6d s.__libc_start_m
      0x00000180 61696e40 40474c49 42435f32 2e322e35 ain@@GLIBC_2.2.5
      0x00000190 005f5f64 6174615f 73746172 74005f5f .__data_start.__
      0x000001a0 676d6f6e 5f737461 72745f5f 005f5f64 gmon_start__.__d
      0x000001b0 736f5f68 616e646c 65005f49 4f5f7374 so_handle._IO_st
      0x000001c0 64696e5f 75736564 005f5f6c 6962635f din_used.__libc_
      0x000001d0 6373755f 696e6974 005f5f62 73735f73 csu_init.__bss_s
      0x000001e0 74617274 006d6169 6e005f4a 765f5265 tart.main._Jv_Re
      0x000001f0 67697374 6572436c 61737365 73005f5f gisterClasses.__
      0x00000200 544d435f 454e445f 5f005f49 544d5f72 TMC_END__._ITM_r
      0x00000210 65676973 74657254 4d436c6f 6e655461 egisterTMCloneTa
      0x00000220 626c6500                            ble.

 - 上面结果中的十六进制数据部分从右到左看是地址递增的方向，而字符内容部分从左到右看是地址递增的方向。

 - 可以在字符串表里找到函数名 addTwoIntegers

 - 符号表 .symtab section 中，有一个条目是用来描述符号 addTwoIntegers的，那么在该条目中就会有一个字段(st_name)记录着字符串 addTwoIntegers 在 .strtab section中的索引。

 - .shstrtab 也是字符串表，只不过其中存储的是 section 的名字，而非所函数或者变量的名称。

 - 字符串表在真正链接和生成进程映像过程中是不需要使用的，但是对调试程序就特别有帮助，前面使用objdump来反汇编.text section 的时候，之所以能看到定义了函数 addTwoIntegers，是因为存在这个字符串表的原因。符号表 .symtab section 在其中作为中介，也起到关键作用。

## .symtab section

 使用
```
readelf -s ./a.out
```

命令可以读取elf文件的.symtab section。内容如下

      （节选了部分）
      Symbol table '.symtab' contains 68 entries:
       Num:    Value          Size Type    Bind   Vis      Ndx Name
         0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND 
         1: 0000000000400238     0 SECTION LOCAL  DEFAULT    1 
        49: 0000000000601028     0 NOTYPE  WEAK   DEFAULT   25 data_start
        50: 0000000000601038     0 NOTYPE  GLOBAL DEFAULT   25 _edata
        51: 00000000004005f4     0 FUNC    GLOBAL DEFAULT   15 _fini
        52: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND printf@@GLIBC_2.2.5
        53: 0000000000400526    20 FUNC    GLOBAL DEFAULT   14 addTwoIntegers
        54: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@@GLIBC_
        55: 0000000000601028     0 NOTYPE  GLOBAL DEFAULT   25 __data_start
        56: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
        57: 0000000000601030     0 OBJECT  GLOBAL HIDDEN    25 __dso_handle
        58: 0000000000400600     4 OBJECT  GLOBAL DEFAULT   16 _IO_stdin_used
        59: 0000000000400580   101 FUNC    GLOBAL DEFAULT   14 __libc_csu_init
        60: 0000000000601040     0 NOTYPE  GLOBAL DEFAULT   26 _end
        61: 0000000000400430    42 FUNC    GLOBAL DEFAULT   14 _start
        62: 0000000000601038     0 NOTYPE  GLOBAL DEFAULT   26 __bss_start
        63: 000000000040053a    67 FUNC    GLOBAL DEFAULT   14 main
        64: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _Jv_RegisterClasses
        65: 0000000000601038     0 OBJECT  GLOBAL HIDDEN    25 __TMC_END__
        66: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
        67: 00000000004003c8     0 FUNC    GLOBAL DEFAULT   11 _init

 - FUNC类型表示函数，可以找到自己的函数addTwoIntegers，还可以看到它在字符串表中的偏移
 - OBJECT 表示和该符号对应的是一个数据对象，比方程序中定义过的变量、数组等，
 - SECTION 表示该符号和一个 section 相关，这种符号用于重定位。
 - 在可执行文件或者动态库中，符号的值表示的是运行时的内存地址