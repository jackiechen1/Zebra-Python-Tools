// initializer
(W)      mov (4|M0)               r20.0<1>:d    0x03020100:uv
(W)      mov (4|M0)               r20.4<1>:d    0x07060504:uv
(W)      mov (4|M0)               r20.8<1>:d    0x0b0a0908:uv
(W)      mov (4|M0)               r20.12<1>:d   0x0f0e0d0c:uv

// src0 (8x16), 128 fp32s
(W)      mov (16|M0)              r3.0<1>:f    r20.0<1;1,0>:d
(W)      add (16|M0)              r4.0<1>:f    r3.0<1;1,0>:f  1.0:f
(W)      add (16|M0)              r5.0<1>:f    r4.0<1;1,0>:f  2.0:f
(W)      add (16|M0)              r6.0<1>:f    r5.0<1;1,0>:f  3.0:f
(W)      add (16|M0)              r7.0<1>:f    r6.0<1;1,0>:f  4.0:f
(W)      add (16|M0)              r8.0<1>:f    r7.0<1;1,0>:f  5.0:f
(W)      add (16|M0)              r9.0<1>:f    r8.0<1;1,0>:f  6.0:f
(W)      add (16|M0)              r10.0<1>:f    r9.0<1;1,0>:f  7.0:f

// ?? - doesn't do anything useful
(W)      mov (16|M0)              r14.0<2>:hf   1.0:hf
(W)      mov (16|M0)              r14.1<2>:hf   1.0:hf

// B
// src1 (16x16), 256 fp16s
(W)      mov (16|M0)               r21.0<1>:hf    r3.0<1;1,0>:f
(W)      mov (16|M0)               r21.16<1>:hf   r4.0<1;1,0>:f
(W)      mov (16|M0)               r22.0<1>:hf    r5<1;1,0>:f
(W)      mov (16|M0)               r22.16<1>:hf   r6<1;1,0>:f
(W)      mov (16|M0)               r23.0<1>:hf    r7<1;1,0>:f
(W)      mov (16|M0)               r23.16<1>:hf   r8<1;1,0>:f
(W)      mov (16|M0)               r24.0<1>:hf    r9<1;1,0>:f
(W)      mov (16|M0)               r24.16<1>:hf   r10<1;1,0>:f

(W)      mov (16|M0)               r25.0<1>:hf    r3.0<1;1,0>:f
(W)      mov (16|M0)               r25.16<1>:hf   r4.0<1;1,0>:f
(W)      mov (16|M0)               r26.0<1>:hf    r5<1;1,0>:f
(W)      mov (16|M0)               r26.16<1>:hf   r6<1;1,0>:f
(W)      mov (16|M0)               r27.0<1>:hf    r7<1;1,0>:f
(W)      mov (16|M0)               r27.16<1>:hf   r8<1;1,0>:f
(W)      mov (16|M0)               r28.0<1>:hf    r9<1;1,0>:f
(W)      mov (16|M0)               r28.16<1>:hf   r10<1;1,0>:f

// rearrange into groups
// r12 is the temp register
(W)      mov (16|M0)               r12.0<1>:ud    r21.0<1;1,0>:ud
(W)      mov (16|M0)               r21.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r21.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r22.0<1;1,0>:ud
(W)      mov (16|M0)               r22.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r22.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r23.0<1;1,0>:ud
(W)      mov (16|M0)               r23.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r23.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r24.0<1;1,0>:ud
(W)      mov (16|M0)               r24.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r24.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r25.0<1;1,0>:ud
(W)      mov (16|M0)               r25.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r25.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r26.0<1;1,0>:ud
(W)      mov (16|M0)               r26.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r26.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r27.0<1;1,0>:ud
(W)      mov (16|M0)               r27.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r27.1<2>:hf    r12.16<1;1,0>:hf

(W)      mov (16|M0)               r12.0<1>:ud    r28.0<1;1,0>:ud
(W)      mov (16|M0)               r28.0<2>:hf    r12.0<1;1,0>:hf
(W)      mov (16|M0)               r28.1<2>:hf    r12.16<1;1,0>:hf

// A
// src2
(W)      mov (16|M0)               r31.0<1>:hf    r3.0<1;1,0>:f
(W)      mov (16|M0)               r31.16<1>:hf   r4.0<1;1,0>:f
(W)      mov (16|M0)               r32.0<1>:hf    r5<1;1,0>:f
(W)      mov (16|M0)               r32.16<1>:hf   r6<1;1,0>:f
(W)      mov (16|M0)               r33.0<1>:hf    r7<1;1,0>:f
(W)      mov (16|M0)               r33.16<1>:hf   r8<1;1,0>:f
(W)      mov (16|M0)               r34.0<1>:hf    r9<1;1,0>:f
(W)      mov (16|M0)               r34.16<1>:hf   r10<1;1,0>:f


// zero out the accum for now
(W)      mov (16|M0)              r3.0<1>:f    0:uw
(W)      mov (16|M0)              r4.0<1>:f    0:uw
(W)      mov (16|M0)              r5.0<1>:f    0:uw
(W)      mov (16|M0)              r6.0<1>:f    0:uw
(W)      mov (16|M0)              r7.0<1>:f    0:uw
(W)      mov (16|M0)              r8.0<1>:f    0:uw
(W)      mov (16|M0)              r9.0<1>:f    0:uw
(W)      mov (16|M0)              r10.0<1>:f   0:uw


//                                                src0 == null := +0.0
// (W)      mov (16|M0)              r3.0<1>:f    null

//                                     C                B                 A
//                       dst           src0             src1              src2
dpas.8x8 (16|M0)         r50:f         r3:f             r21:hf            r31.0:hf

/*

this should be 8x16 + 8x16 * 16x16

M = 8 (because of the repeat count)
N = 16 (because of exec size)
K = 16 (because fp16)

               A(MxK) x B(KxN) [+ C(MxN)]

dpas dst src0 src1 src2
               B    A

?? <1;1,0>

r50.0<1>:f = r3.0<1;1,0>:f +
  r21.0<2;2,1>:hf . r31.0<0;2,1>:hf +           ... + broadcast 2 fp16
  r22.0<2;2,1>:hf . r31.2<0;2,1>:hf +
  r23.0<2;2,1>:hf . r31.4<0;2,1>:hf +
  r24.0<2;2,1>:hf . r31.6<0;2,1>:hf +
  r25.0<2;2,1>:hf . r31.8<0;2,1>:hf +
  r26.0<2;2,1>:hf . r31.10<0;2,1>:hf +
  r27.0<2;2,1>:hf . r31.12<0;2,1>:hf +
  r28.0<2;2,1>:hf . r31.14<0;2,1>:hf
r51.0<1>:f = r4.0<1;1,0>:f +
  r21.0<2;2,1>:hf . r31.16<0;2,1>:hf +
  r22.0<2;2,1>:hf . r31.18<0;2,1>:hf +
  r23.0<2;2,1>:hf . r31.20<0;2,1>:hf +
  r24.0<2;2,1>:hf . r31.22<0;2,1>:hf +
  r25.0<2;2,1>:hf . r31.24<0;2,1>:hf +
  r26.0<2;2,1>:hf . r31.26<0;2,1>:hf +
  r27.0<2;2,1>:hf . r31.28<0;2,1>:hf +
  r28.0<2;2,1>:hf . r31.30<0;2,1>:hf
r52.0<1>:f = r5.0<1;1,0>:f +
  r21.0<2;2,1>:hf . r32.0<0;2,1>:hf +
  r22.0<2;2,1>:hf . r32.2<0;2,1>:hf +
  r23.0<2;2,1>:hf . r32.4<0;2,1>:hf +
  r24.0<2;2,1>:hf . r32.6<0;2,1>:hf +
  r25.0<2;2,1>:hf . r32.8<0;2,1>:hf +
  r26.0<2;2,1>:hf . r32.10<0;2,1>:hf +
  r27.0<2;2,1>:hf . r32.12<0;2,1>:hf +
  r28.0<2;2,1>:hf . r32.14<0;2,1>:hf
r53.0<1>:f = r6.0<1;1,0>:f +
  r21.0<2;2,1>:hf . r32.16<0;2,1>:hf +
  r22.0<2;2,1>:hf . r32.18<0;2,1>:hf +
  r23.0<2;2,1>:hf . r32.20<0;2,1>:hf +
  r24.0<2;2,1>:hf . r32.22<0;2,1>:hf +
  r25.0<2;2,1>:hf . r32.24<0;2,1>:hf +
  r26.0<2;2,1>:hf . r32.26<0;2,1>:hf +
  r27.0<2;2,1>:hf . r32.28<0;2,1>:hf +
  r28.0<2;2,1>:hf . r32.30<0;2,1>:hf

// and 4 more (for repeat count = 8)

*/

// result
// D0129FFF D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 D012A000 r5
// D01F5FFE D01F5FFE D01F5FFE D01F5FFF D01F6000 D01F6000 D01F6000 D01F6000 D01F5FFF D01F6000 D01F6000 D01F6000 D01F6000 D01F6000 D01F6000 D01F6000 r6
// D038DFFE D038DFFE D038DFFE D038DFFE D038DFFE D038DFFF D038DFFF D038E000 D038DFFE D038DFFE D038DFFE D038DFFF D038E000 D038E000 D038E000 D038E000 r7
// D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFF D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFE D05F1FFF D05F1FFF D05F2000 r8
// D0890FFE D0890FFE D0890FFE D0890FFE D0890FFE D0890FFE D0891000 D0891000 D0890FFE D0890FFE D0890FFE D0890FFF D0891000 D0891000 D0891000 D0891000 r9
// D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFF D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFE D0A8EFFF D0A8F000 D0A8F000 r10
// D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFE D0CF2FFF r11
// D0FBCFFC D0FBCFFD D0FBCFFD D0FBCFFD D0FBCFFD D0FBCFFD D0FBCFFE D0FBCFFE D0FBCFFD D0FBCFFD D0FBCFFD D0FBCFFE D0FBCFFE D0FBCFFE D0FBCFFE D0FBCFFF r12

//dpas.8x8 (16|M0)         r15:hf         r5:f             r21:hf            r31.0:hf

// fulsim result
// D09FD09F D09FD09F D09FD09F D09FD09F D09FD09F D09FD09F D09FD09F D09FD09F D093D093 D093D093 D093D093 D093D093 D093D093 D093D093 D093D093 D093D093 r15
// D0DFD0DF D0DFD0DF D0DFD0DF D0DFD0DF D0DFD0DF D0DFD0DF D0DFD0DF D0DFD0DF D0B9D0B9 D0B9D0B9 D0B9D0B9 D0B9D0B9 D0B9D0B9 D0B9D0B9 D0B9D0B9 D0B9D0B9 r16
// D129D129 D129D129 D129D129 D129D129 D129D129 D129D129 D129D129 D129D129 D109D109 D109D109 D109D109 D109D109 D109D109 D109D109 D109D109 D109D109 r17
// D17CD17C D17CD17C D17CD17C D17CD17C D17CD17C D17CD17C D17CD17C D17CD17C D14FD14F D14FD14F D14FD14F D14FD14F D14FD14F D14FD14F D14FD14F D14FD14F r18

