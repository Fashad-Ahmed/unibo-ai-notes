The Concept: KV Caching & PagedAttention

When an LLM generates text, it does it autoregressively (one token at a time).

1. The Compute vs. Memory Problem

During training, the model processes the entire document in parallel. Massive matrix multiplications keep the GPU's compute cores at 100% utilization.During generation (inference), the model only generates one token, $x_t$. To predict $x_{t+1}$, the Attention mechanism must calculate the dot product of the new token's Query ($Q$) against the Keys ($K$) and Values ($V$) of all past tokens.Recomputing $K$ and $V$ for all past tokens at every single step is computationally suicidal.



2. The KV Cache Solution

To solve this, engineers created the KV Cache. We store the mathematically computed $K$ and $V$ vectors for every token in the GPU's High Bandwidth Memory (HBM). When the next token is generated, we just fetch the cached vectors.The Catch: An LLM is no longer compute-bound; it is memory-bandwidth bound. The GPU cores sit idle waiting for massive gigabytes of KV tensors to be transferred from the VRAM into the SRAM for every single word.


3. The Fragmentation Crisis


Because sentence lengths are unpredictable, standard inference engines (like HuggingFace) pre-allocate a contiguous block of memory for the maximum possible sequence length (e.g., 2048 tokens) for every user request.

If a user's prompt and response only total 50 tokens, the remaining 1,998 tokens of allocated memory are completely wasted.

Research showed that up to 60% to 80% of GPU memory was being wasted due to internal and external fragmentation. You couldn't serve more users because your memory was full of "empty space."



4. The Breakthrough: PagedAttention


In 2023, researchers realized this is the exact same problem operating systems faced decades ago with RAM. Their solution was to bring Virtual Memory and Paging to the Deep Learning KV Cache.

Instead of allocating one massive, contiguous block of memory for a sequence, PagedAttention chops the KV cache into fixed-size "blocks" (e.g., 16 tokens per block).

Logical vs. Physical: The tokens appear continuous to the LLM's mathematical attention mechanism (Logical View), but they are actually scattered non-contiguously across the GPU's memory (Physical View).

The Page Table: A dynamic Block Table maps the logical tokens to their physical blocks. Memory is only allocated exactly when a block is filled.

The Result: Memory waste dropped from 60% to under 4%. This single system design breakthrough allowed servers to batch 4x to 5x more concurrent users on the exact same GPU hardware.