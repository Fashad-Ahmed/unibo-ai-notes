#include "pmsis.h"


// generic matrix multiplication
void gemm(int * MatA, int * MatB, int* MatC, int NN, int MM, int KK){
    uint32_t core_id, i_chunk, i_start, i_end;
    uint32_t i = 0;

    core_id = pi_core_id();
    i_chunk = (NN + NUM_CORES-1) / NUM_CORES;
    i_start = core_id * i_chunk;
    i_end   = i_start + i_chunk < NN ? i_start + i_chunk : NN;

  #ifdef TRACE_EXECUTION
    printf("[trace] core %d: processing rows [%d, %d)\n", core_id, i_start, i_end);
  #endif

    // task to profile
    for (i = i_start; i < i_end; i ++) {
      for (int j = 0; j < MM; j++) {
        int acc = 0;
        for (int k = 0; k < KK; k++) {
          acc += MatA[i*KK+k] * MatB[k*MM+j];
        } //k
        MatC[i*MM+j] = acc;
      }//j
    }//i
#ifdef TRACE_EXECUTION
    printf("[trace] core %d: finished rows [%d, %d)\n", core_id, i_start, i_end);
#endif
    pi_cl_team_barrier();

}


/* TASK 1.3: Loop unrolling technique
 *
 * Does the scheduling of the instructions avoid the stalls?
 * If you have the following pattern:
 *
 * lw A, off(B)
 * lw C, off(D)
 * lw E, off(F)
 * lw G, off(H)
 * mac A, C, Z
 * mac E, G, Y
 *
 * would there be any load stall?
 * This approach is known as loop unrolling. This method is
 * one of the most powerful technique you have to optimize code.
 * Especially in regular accesses tasks such as array operations,
 * loops might be always unrolled and, in fact, the compiler tends
 * to apply the unrolling whenever he can.
 *
 * 1.3.2: Implement loop unrolling with factor of 2, 4, 8, 16 and
 * fill the table with the overall MACs/cycle for 8 cores execution.
 * Do you see a regression doing more aggressive loop unrolling? Why?
 * Look at the stalls, but also at the instructions and the cycles: fewer
 * stalls do not always mean fewer cycles. With K=16, the unrolled inner
 * loop runs only a few iterations (2 with factor 8), so the setup code
 * around it weighs more and more on the total.
 * Another problem is that implementing unrolling, you are forcing multiple
 * loads from the memory, loading the values in the internal core
 * registers. They are not infinite, especially in embedded architecture
 * such as PULP. The available registers in the register file
 * of the core are 32, but not all are general purpose registers.
 * This fact actually limits the unrolling, because, if you saturate
 * the available registers in your architecture, you would face with
 * spilling issues, where the compiler pushes and pops over and over
 * to and from the stack (memory) the values on the registers to reuse
 * the register for another operand. This effect would destroy all the
 * performance metrics.
 */
void gemm_unroll(int * MatA, int * MatB, int* MatC, int NN, int MM, int KK){
    uint32_t core_id = pi_core_id();
    uint32_t i_chunk = (NN + NUM_CORES - 1) / NUM_CORES;
    uint32_t i_start = core_id * i_chunk;
    uint32_t i_end = i_start + i_chunk < NN ? i_start + i_chunk : NN;

#if UNROLL_FACTOR != 2 && UNROLL_FACTOR != 4 && UNROLL_FACTOR != 8 && UNROLL_FACTOR != 16
#error UNROLL_FACTOR must be 2, 4, 8, or 16
#endif

    for (int i = i_start; i < i_end; i++) {
      for (int j = 0; j < MM; j++) {
        int acc = 0;
        int k = 0;
        for (; k + UNROLL_FACTOR <= KK; k += UNROLL_FACTOR) {
#if UNROLL_FACTOR >= 2
          int a0 = MatA[i * KK + k + 0];
          int a1 = MatA[i * KK + k + 1];
#endif
#if UNROLL_FACTOR >= 4
          int a2 = MatA[i * KK + k + 2];
          int a3 = MatA[i * KK + k + 3];
#endif
#if UNROLL_FACTOR >= 8
          int a4 = MatA[i * KK + k + 4];
          int a5 = MatA[i * KK + k + 5];
          int a6 = MatA[i * KK + k + 6];
          int a7 = MatA[i * KK + k + 7];
#endif
#if UNROLL_FACTOR >= 16
          int a8 = MatA[i * KK + k + 8];
          int a9 = MatA[i * KK + k + 9];
          int a10 = MatA[i * KK + k + 10];
          int a11 = MatA[i * KK + k + 11];
          int a12 = MatA[i * KK + k + 12];
          int a13 = MatA[i * KK + k + 13];
          int a14 = MatA[i * KK + k + 14];
          int a15 = MatA[i * KK + k + 15];
#endif
#if UNROLL_FACTOR >= 2
          int b0 = MatB[(k + 0) * MM + j];
          int b1 = MatB[(k + 1) * MM + j];
#endif
#if UNROLL_FACTOR >= 4
          int b2 = MatB[(k + 2) * MM + j];
          int b3 = MatB[(k + 3) * MM + j];
#endif
#if UNROLL_FACTOR >= 8
          int b4 = MatB[(k + 4) * MM + j];
          int b5 = MatB[(k + 5) * MM + j];
          int b6 = MatB[(k + 6) * MM + j];
          int b7 = MatB[(k + 7) * MM + j];
#endif
#if UNROLL_FACTOR >= 16
          int b8 = MatB[(k + 8) * MM + j];
          int b9 = MatB[(k + 9) * MM + j];
          int b10 = MatB[(k + 10) * MM + j];
          int b11 = MatB[(k + 11) * MM + j];
          int b12 = MatB[(k + 12) * MM + j];
          int b13 = MatB[(k + 13) * MM + j];
          int b14 = MatB[(k + 14) * MM + j];
          int b15 = MatB[(k + 15) * MM + j];
#endif

          asm volatile("" ::: "memory");

#if UNROLL_FACTOR >= 2
          acc += a0 * b0;
          acc += a1 * b1;
#endif
#if UNROLL_FACTOR >= 4
          acc += a2 * b2;
          acc += a3 * b3;
#endif
#if UNROLL_FACTOR >= 8
          acc += a4 * b4;
          acc += a5 * b5;
          acc += a6 * b6;
          acc += a7 * b7;
#endif
#if UNROLL_FACTOR >= 16
          acc += a8 * b8;
          acc += a9 * b9;
          acc += a10 * b10;
          acc += a11 * b11;
          acc += a12 * b12;
          acc += a13 * b13;
          acc += a14 * b14;
          acc += a15 * b15;
#endif
        }

        for (; k < KK; k++) {
          acc += MatA[i * KK + k] * MatB[k * MM + j];
        }
        MatC[i * MM + j] = acc;
      }
    }
    pi_cl_team_barrier();
}
