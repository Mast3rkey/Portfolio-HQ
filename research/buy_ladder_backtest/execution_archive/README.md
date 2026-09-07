# LADDER-V2-0001 complete execution bundle

This directory stores the immutable registered execution as deterministic,
fixed-size archive parts so that the full daily paths and sensitivity ledgers
remain reviewable without committing individual near-limit Git blobs.

The human-readable decision files remain beside the archive directory under
`../execution/`. The archive contains all eleven original output files, with
their exact filenames and bytes. Their SHA-256 values are pinned by
`../execution/input_manifest.json`.

To reconstruct the original bundle from the repository root:

```bash
cat research/buy_ladder_backtest/execution_archive/LADDER-V2-0001-complete.tar.zst.part-* \
  > /tmp/LADDER-V2-0001-complete.tar.zst
sha256sum -c research/buy_ladder_backtest/execution_archive/SHA256SUMS --ignore-missing
mkdir -p /tmp/LADDER-V2-0001
tar --use-compress-program=unzstd -xf /tmp/LADDER-V2-0001-complete.tar.zst \
  -C /tmp/LADDER-V2-0001
```

Then run the independent validator against the reconstructed `execution`
directory. The archive is packaging only: it does not alter the registered
inputs, calculations, disposition, or advisory-only boundary.
