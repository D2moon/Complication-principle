assume  cs:code
code    segment
MOV  AX,  123BH
MOV  DS,   AX
MOV  AX,  1000H
MOV  SS,  AX
MOV  SP,  0010H
LD BX, 0x64H
LD CX, 0xaH
ST BX, [0x12]
ST CX, [0x10]
MOV AX, 4C00H
INT 21H
code ends
end
