# Impossible Password

Once extracted, we have the `impossible_password.bin` file. Let's see what type it is.
```
file impossible_password.bin
impossible_password.bin: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=ba116ba1912a8c3779ddeb579404e2fdf34b1568, stripped
```

It’s an `ELF 64-bit LSB` executable.

Strings inside the `.data` section
```
rabin2 -z impossible_password.bin
[Strings]
nth paddr      vaddr      len size section type  string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x00000a70 0x00400a70 14  15   .rodata ascii SuperSeKretKey
1   0x00000a82 0x00400a82 4   5    .rodata ascii %20s
2   0x00000a87 0x00400a87 5   6    .rodata ascii [%s]\n
```

`SuperSeKretKey` appears to be interesting

# Execution
```
chmod +x impossible_password.bin
./impossible_password.bin
* SuperSeKretKey
[SuperSeKretKey]
** WhatShouldIWrite?
```

By executing this program, a star `(*)` is displayed. I want to write `SuperSeKretKey` because the string displayed in the `.data` section informs us that the string (`%s`) is manipulated. Indeed, when I put SuperSeKretKey, this text is surrounded with `[]`.

After this, two stars `(**)` are displayed. I’ve tried to write many things (as WhatShouldIWrite?), but the program always terminates

It looks like the program is waiting for a specific string, but I don’t know what it is.

# Reverse engineering
<i>Let's use Radare2</i>

Perform analysis :
```
radare2 impossible_password.bin
[0x004006a0]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Check for objc references
[x] Check for vtables
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Finding function preludes
[x] Enable constraint types analysis for variables
```
Change memory address to main function :
```
[0x004006a0]> s main
[0x0040085d]>
```
The focus is now at the `main()` address: `0x0040085d`.

# Disassemble

With the `pdf` command, disassemble the `main()` code 

> pdf => `print disassemble function`

```
[0x0040085d]> pdf
            ; DATA XREF from entry0 @ 0x4006bd
┌ 283: int main (int argc, char **argv);
│           ; var int64_t var_50h @ rbp-0x50
│           ; var int64_t var_44h @ rbp-0x44
│           ; var int64_t var_40h @ rbp-0x40
│           ; var int64_t var_3fh @ rbp-0x3f
│           ; var int64_t var_3eh @ rbp-0x3e
│           ; var int64_t var_3dh @ rbp-0x3d
│           ; var int64_t var_3ch @ rbp-0x3c
│           ; var int64_t var_3bh @ rbp-0x3b
│           ; var int64_t var_3ah @ rbp-0x3a
│           ; var int64_t var_39h @ rbp-0x39
│           ; var int64_t var_38h @ rbp-0x38
│           ; var int64_t var_37h @ rbp-0x37
│           ; var int64_t var_36h @ rbp-0x36
│           ; var int64_t var_35h @ rbp-0x35
│           ; var int64_t var_34h @ rbp-0x34
│           ; var int64_t var_33h @ rbp-0x33
│           ; var int64_t var_32h @ rbp-0x32
│           ; var int64_t var_31h @ rbp-0x31
│           ; var int64_t var_30h @ rbp-0x30
│           ; var int64_t var_2fh @ rbp-0x2f
│           ; var int64_t var_2eh @ rbp-0x2e
│           ; var int64_t var_2dh @ rbp-0x2d
│           ; var int64_t var_20h @ rbp-0x20
│           ; var int64_t var_ch @ rbp-0xc
│           ; var int64_t var_8h @ rbp-0x8
│           ; arg int argc @ rdi
│           ; arg char **argv @ rsi
│           0x0040085d      55             push rbp
│           0x0040085e      4889e5         mov rbp, rsp
│           0x00400861      4883ec50       sub rsp, 0x50
│           0x00400865      897dbc         mov dword [var_44h], edi    ; argc
│           0x00400868      488975b0       mov qword [var_50h], rsi    ; argv
│           0x0040086c      48c745f8700a.  mov qword [var_8h], str.SuperSeKretKey ; 0x400a70 ; "SuperSeKretKey"
│           0x00400874      c645c041       mov byte [var_40h], 0x41    ; 'A' ; 65
│           0x00400878      c645c15d       mov byte [var_3fh], 0x5d    ; ']' ; 93
│           0x0040087c      c645c24b       mov byte [var_3eh], 0x4b    ; 'K' ; 75
│           0x00400880      c645c372       mov byte [var_3dh], 0x72    ; 'r' ; 114
│           0x00400884      c645c43d       mov byte [var_3ch], 0x3d    ; '=' ; 61
│           0x00400888      c645c539       mov byte [var_3bh], 0x39    ; '9' ; 57
│           0x0040088c      c645c66b       mov byte [var_3ah], 0x6b    ; 'k' ; 107
│           0x00400890      c645c730       mov byte [var_39h], 0x30    ; '0' ; 48
│           0x00400894      c645c83d       mov byte [var_38h], 0x3d    ; '=' ; 61
│           0x00400898      c645c930       mov byte [var_37h], 0x30    ; '0' ; 48
│           0x0040089c      c645ca6f       mov byte [var_36h], 0x6f    ; 'o' ; 111
│           0x004008a0      c645cb30       mov byte [var_35h], 0x30    ; '0' ; 48
│           0x004008a4      c645cc3b       mov byte [var_34h], 0x3b    ; ';' ; 59
│           0x004008a8      c645cd6b       mov byte [var_33h], 0x6b    ; 'k' ; 107
│           0x004008ac      c645ce31       mov byte [var_32h], 0x31    ; '1' ; 49
│           0x004008b0      c645cf3f       mov byte [var_31h], 0x3f    ; '?' ; 63
│           0x004008b4      c645d06b       mov byte [var_30h], 0x6b    ; 'k' ; 107
│           0x004008b8      c645d138       mov byte [var_2fh], 0x38    ; '8' ; 56
│           0x004008bc      c645d231       mov byte [var_2eh], 0x31    ; '1' ; 49
│           0x004008c0      c645d374       mov byte [var_2dh], 0x74    ; 't' ; 116
│           0x004008c4      bf7f0a4000     mov edi, 0x400a7f           ; const char *format
│           0x004008c9      b800000000     mov eax, 0
│           0x004008ce      e82dfdffff     call sym.imp.printf         ; int printf(const char *format)
│           0x004008d3      488d45e0       lea rax, [var_20h]
│           0x004008d7      4889c6         mov rsi, rax
│           0x004008da      bf820a4000     mov edi, str.20s            ; 0x400a82 ; "%20s" ; const char *format
│           0x004008df      b800000000     mov eax, 0
│           0x004008e4      e887fdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x004008e9      488d45e0       lea rax, [var_20h]
│           0x004008ed      4889c6         mov rsi, rax
│           0x004008f0      bf870a4000     mov edi, str.s              ; 0x400a87 ; "[%s]\n" ; const char *format
│           0x004008f5      b800000000     mov eax, 0
│           0x004008fa      e801fdffff     call sym.imp.printf         ; int printf(const char *format)
│           0x004008ff      488b55f8       mov rdx, qword [var_8h]
│           0x00400903      488d45e0       lea rax, [var_20h]
│           0x00400907      4889d6         mov rsi, rdx                ; const char *s2
│           0x0040090a      4889c7         mov rdi, rax                ; const char *s1
│           0x0040090d      e81efdffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│           0x00400912      8945f4         mov dword [var_ch], eax
│           0x00400915      837df400       cmp dword [var_ch], 0
│       ┌─< 0x00400919      740a           je 0x400925
│       │   0x0040091b      bf01000000     mov edi, 1                  ; int status
│       │   0x00400920      e85bfdffff     call sym.imp.exit           ; void exit(int status)
│       │   ; CODE XREF from main @ 0x400919
│       └─> 0x00400925      bf8d0a4000     mov edi, 0x400a8d           ; const char *format
│           0x0040092a      b800000000     mov eax, 0
│           0x0040092f      e8ccfcffff     call sym.imp.printf         ; int printf(const char *format)
│           0x00400934      488d45e0       lea rax, [var_20h]
│           0x00400938      4889c6         mov rsi, rax
│           0x0040093b      bf820a4000     mov edi, str.20s            ; 0x400a82 ; "%20s" ; const char *format
│           0x00400940      b800000000     mov eax, 0
│           0x00400945      e826fdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x0040094a      bf14000000     mov edi, 0x14               ; 20 ; size_t arg1
│           0x0040094f      e839feffff     call fcn.0040078d
│           0x00400954      4889c2         mov rdx, rax
│           0x00400957      488d45e0       lea rax, [var_20h]
│           0x0040095b      4889d6         mov rsi, rdx                ; const char *s2
│           0x0040095e      4889c7         mov rdi, rax                ; const char *s1
│           0x00400961      e8cafcffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│           0x00400966      85c0           test eax, eax
│       ┌─< 0x00400968      750c           jne 0x400976
│       │   0x0040096a      488d45c0       lea rax, [var_40h]
│       │   0x0040096e      4889c7         mov rdi, rax                ; int64_t arg1
│       │   0x00400971      e802000000     call fcn.00400978
│       │   ; CODE XREF from main @ 0x400968
│       └─> 0x00400976      c9             leave
└           0x00400977      c3             ret
```

From `0x0040086c` to `0x00400920` memory addresses, some manipulations are carried out on strings and to be honest, I didn’t try to understand because something popped into my head.

At `0x00400961` memory address, the binary safe string comparison strcmp is performed between `*s1` and `*`s2`.

Let’s talk about the `0x00400968` memory address.

Register `eax` will contain the return code from `strcmp`, after the call. The test `eax`, `eax` is the same as `and` `eax`, `eax` (bitwise and) except that it doesn’t store the result in `eax`. So `eax` isn’t affected by the test, but the `zero-flag (ZF)` is.

The test `eax`, `eax` is necessary to make the jne work in the first place. Also, jne is the same as `jnz`, just as `je` is the same as `jz`. Both act based on the `ZF` value.

The `jne` branch will be taken if `ZF=0` and therefore whenever `strcmp` returns a non-zero value (strings not equal). Conversely if `eax` contains zero upon return from `strcmp`, the jump via `jne` will not happen.

If you have understood everything correctly, `strcmp` compares the strings and sets `eax` to zero if the strings are `equal`. If they are not, the `jne` instruction takes us to the memory address `0x00400976` which is the program’s exit (leave).

# Reopen in read-write
```
[0x0040085d]> oo+
```
Change memory address focus

We want to edit the `jne` section, so let’s jump into this memory address.
```
Change memory address focus
We want to edit the jne section, so let’s jump into this memory address.
```
ASM instruction modification

The easy way to bypass this `jne` is to write `NOP` (`No OPeration`) instruction.
```
[0x00400968]> wx 9090
[0x00400968]> wa nop
Written 1 byte(s) (nop) = wx 90
```
We can see our new instruction by disassembling a new time (the disassemble has been truncated).
```
[0x00400968]> pdf
0x00400961      e8cafcffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
0x00400966      85c0           test eax, eax
0x00400968      90             nop
```
That’s all with `radare2`, we can leave.
```
[0x00400968]> q
```
Execution
```
./impossible_password.bin
* SuperSeKretKey
[SuperSeKretKey]
** plop
HTB{+*+*+*+*+*+*+*+*+*+*+*+*}
```
Affected by: [Adrien](https://illuad.fr/2020/07/16/writeup-htb-reversing-impossible-password.html)