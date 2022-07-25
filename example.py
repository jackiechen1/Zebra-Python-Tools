ExampleText = """add (8|M0)               r11.0<1>:ud   r7.0<1;1,0>:ud r101.0<1;1,0>:ud
mov (16|M0)               r120.0<1>:ud   r127.0<1;1,0>:ud
mov (8|M0)               r105.0<2>:ud   r70.0<1;1,0>:ud
mov (8|M0)               r1.1<2>:ud   r5.0<1;1,0>:ud
mov (8|M0)               r13.0<1>:ud   r79.0<4;2,2>:ud
mov (8|M0)               r16.0<1>:uw   r13.0<8;8,1>:uw"""
ExampleModeLabels = ["This example shows an operation adding 8 elements of r7 and r101 to r11",
                     "This example shows moving 16 elements from r127 to r120",
                     "This example shows the destination (r105) located every other element",
                     "This example shows the destination (r1) adding an offset of one elements",
                     "This example shows the source (r79) changing v,w,h",
                     "This example changes the data type to word (2 bytes)."]