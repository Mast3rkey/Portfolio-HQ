# Portfolio-HQ private owner interface and chart inbox

A private, phone- and tablet-usable view of accepted Portfolio-HQ state, plus a
quarantined inbox for owner-supplied chart images.

**Recommendation-only.** Nothing in this interface places, routes or submits an
order. It holds no brokerage connection, uses no brokerage credential, reads no
live account, and touches no Stage-1 surface.

---

## 1. The scoped architecture change, stated explicitly

The historical presentation contract was deliberately narrow: `portfolio_hq.dashboard`
serves one generated page, over `GET` only, bound to loopback only, and writes
nothing. The owner requirement asks for something that contract cannot provide —
private access from a phone or iPad with the laptop closed, and a way to send a
chart in.

That is a real widening of capability, so it is recorded here rather than
smuggled in by loosening the existing server:

| | Existing dashboard | New owner interface |
|---|---|---|
| Module | `portfolio_hq.dashboard` | `portfolio_hq.owner` |
| Methods | `GET` only; everything else `405` | `GET` and `POST` only |
| Bind | loopback only, enforced in the CLI | loopback **or** a private host |
| Authentication | none (loopback is the boundary) | **mandatory, on every host** |
| Writes | nothing | only inside the chart inbox directory |
| Portfolio calculation | reuses canonical functions in-process | none at all; reads a prebuilt export |

**The existing dashboard is unchanged by this unit.** It was not rebound,
subclassed, wrapped or relaxed. It still refuses `POST`/`PUT`/`DELETE`/`PATCH`
with `405`, and its CLI still rejects any non-loopback `--host`. Both facts are
asserted by tests in `test_portfolio_hq_owner_interface.py`.

## 2. Two halves, one trust boundary

**Build-time (trusted, in-repository).** `portfolio_hq.owner.export` reuses
Portfolio-HQ's own canonical functions — `dashboard.model.build_model`,
`level1_policy_summary.build_policy_summary`, and `allocate`'s
`load_cash_state` / `load_margin_state` / `current_dollar_availability` /
`protected_weights` — and writes one JSON presentation export. It implements no
second allocator and invents no number.

**Runtime (hosted, minimal).** `portfolio_hq.owner.service` serves that JSON to
an authenticated owner and accepts chart images. It imports no investment code
at all: not `allocate`, not `margin_state`, not a brokerage client, not even the
dashboard model. It therefore *cannot* compute a portfolio figure, correct or
otherwise. A test imports the service in a clean subprocess and fails if any of
those modules appears in `sys.modules`.

Concretely, the running service reads exactly two paths — the export file and
the inbox directory — and writes exactly one: inside the inbox.

## 3. Unavailable means unavailable

The export carries no book value, because computing one needs live position
valuation this offline layer deliberately does not have. Rather than estimate,
the export feeds that fact to `allocate.current_dollar_availability` — the
repository's own single gate for "may current dollar figures be published at
all" — and records its verdict and reasons. The interface then shows *why* a
figure is missing and what would restore it. A stale cash or margin observation
is shown as a dated historical observation, never as a current figure.

### Bounded summaries

Some canonical records carry very long narrative text — one workstream's
`next_action` runs to ~59,000 characters. Shipping those whole put ~100 KB of
prose on a phone for a summary view, so free-text summary fields are bounded at
the export layer. Nothing is dropped silently: the shortened text travels with
its true character count and a truncation flag, the page says a note was
shortened and by how much, and the repository file named in the record remains
the complete source. Every owner page is under 35 KB against real state, and a
test fails if that regresses.

## 4. Private access

Authentication is mandatory on **every** host, loopback included. With no token
configured the service refuses to start; there is no anonymous mode to fall back
to and no "it's only localhost" exemption.

* Secret: `PORTFOLIO_HQ_OWNER_TOKEN`, from the environment only. At least 32
  characters. **Never committed** — there is no default and no file in this
  repository that can supply one.
* Generate one with:
  `python -c "import secrets; print(secrets.token_urlsafe(32))"`
* Sign-in exchanges the token for a session cookie: `HttpOnly`, `SameSite=Strict`,
  `Path=/`, and `Secure` whenever the service is bound to anything other than
  loopback. The cookie is an HMAC over its own expiry keyed by the token, so it
  cannot be forged or extended, and **rotating the token immediately invalidates
  every outstanding session**.
* Failed sign-ins are throttled per source address with a fixed lockout window.
  This is a single-instance speed bump, not a distributed rate limiter.
* `POST` requests are refused when an `Origin` header is present and disagrees
  with the `Host` — belt and braces alongside `SameSite=Strict`.
* Responses carry `Content-Security-Policy: default-src 'none'` (with no
  `script-src` at all — the interface ships no JavaScript), `nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store`
  and `robots: noindex`.
* Three routes are reachable without a session, and none of them discloses
  anything: `GET`/`POST /login` (the sign-in form itself), `GET /logout`, and
  `GET /healthz`. `/healthz` exists for a host's health checker and returns
  `{"status": "ok"}` and nothing else — no commit, no ticker, no balance. Every
  route that shows portfolio or chart information requires a valid session.

**TLS is the host's job.** Bind behind a platform that terminates TLS. The
session cookie is marked `Secure` on any non-loopback bind and will simply not
be sent over plain HTTP, so a misconfigured deployment fails closed rather than
leaking a session.

## 5. Chart inbox

Intake is *evidence receipt*, not adoption.

* PNG and JPEG only, decided by inspecting the file's own bytes. A
  client-supplied extension is never trusted, never used to pick a storage
  path, and never used to choose the media type; a mismatch is recorded and
  shown. HEIC/WebP/GIF/SVG/PDF are refused — re-save as PNG or JPEG.
* **The whole byte stream is verified, not just its opening fields.** Reading a
  dimension header proves an image *starts* like a PNG or JPEG; it does not
  prove the bytes form a complete image a reviewer could open. `image_integrity.py`
  therefore verifies every PNG chunk's CRC-32, requires IHDR-first / IEND-last /
  contiguous IDAT, and actually decompresses the image data to check its length
  against the size the header implies (Adam7 interlacing included); and it walks
  the whole JPEG marker stream, requiring a frame header, at least one scan with
  non-empty entropy-coded data (byte-stuffing and restart markers handled) and a
  terminating EOI. Truncated, corrupt, short-raster and header-only files are
  refused. This is standard-library only: a native image library on an
  untrusted-input boundary is the wrong trade, and it would break the hosted
  service's standard-library-only property. Where the two differ, the inbox is
  deliberately **stricter** than a lenient decoder — some incomplete files still
  render in Pillow and are still refused here, because evidence that silently
  misrepresents itself is worse than no evidence.
* Bounded size, checked twice: the request is refused on its declared
  `Content-Length` before a byte of payload is read, and the payload is
  re-checked against the inbox ceiling. A PNG declaring impossible dimensions is
  refused from its header arithmetic, so a decompression bomb never sizes a
  buffer from attacker-supplied numbers.
* Storage identity is server-generated (UTC timestamp plus random hex) and
  matched against a strict pattern before it is ever joined to a path. The
  stored filename is a fixed constant. A hostile filename survives only as
  sanitised display text.
* **Storage is contained, checked by resolution rather than by string prefix.**
  `mkdir` and `open` both follow a symlinked *parent*, so a symlink at
  `charts` would place the intake directory, the image and the record outside
  the configured inbox while the record still claimed an inbox-relative path.
  The charts directory is refused if it is a symlink or resolves anywhere but
  to itself, and every read path fails closed the same way. A symlinked *inbox
  root* remains legitimate — an operator may point it at a mounted volume — so
  the root is resolved first and the result treated as authoritative.
* **A failed intake publishes nothing.** The intake is assembled in a private
  `.incoming/` staging directory and moved into place with a single atomic
  rename; any failure removes the staging tree and nothing else. Previously a
  late failure writing the record left the image bytes behind, so the owner was
  told the chart was *not* received while its bytes stayed on the volume,
  invisible to the index and ambiguous for future duplicate detection.
* Directories are created with `exist_ok=False` and files opened `O_EXCL`, so a
  collision fails loudly instead of overwriting.
* Bytes are retained **exactly** as received — the multipart splitter copies
  payload slices verbatim rather than delegating to a text-oriented parser that
  might normalise line endings and invalidate the recorded SHA-256.
* Duplicate content is detected by hash, recorded for visibility, and **not**
  stored a second time.
* A rejection writes nothing at all — no record, no bytes — so a clumsy or
  hostile caller cannot fill the volume.
* Every stored record carries an explicit `influence` block asserting that
  receipt changes no portfolio membership, no Level-1 or Level-2 target, no
  policy, cap or cluster, no margin doctrine, no holding, no Stage-1 state and
  no order.
* A retained original can be fetched back for review at
  `/charts/image/<intake-id>`, so the inbox has a working reviewer handoff
  rather than being a write-only hole.

**Not in this unit:** chart interpretation, review-state transitions, and any
path from a chart to a recommendation. No production chart batch is requested.

## 6. Running it

```bash
# 1. Build the presentation export from an accepted repository state.
python -m portfolio_hq.owner export --output var/owner/export.json

# 2. Serve it privately. A token is mandatory.
export PORTFOLIO_HQ_OWNER_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python -m portfolio_hq.owner serve \
    --export var/owner/export.json \
    --inbox  var/owner/inbox \
    --host 127.0.0.1 --port 8080
```

`var/` is gitignored: the export and the inbox are runtime state, never
repository truth, and are never committed.

Rebuild the export whenever the accepted repository state changes. A missing or
unreadable export does not stop the service — the interface says plainly that it
has not been built, and chart intake still works.

## 7. Deploying to a private host

The runtime half needs **only the Python standard library**, so it runs on any
small private host. `deploy/owner_interface/Dockerfile` builds it provider-neutrally.

```bash
docker build -f deploy/owner_interface/Dockerfile -t portfolio-hq-owner .
docker run --rm -p 8080:8080 \
  -e PORTFOLIO_HQ_OWNER_TOKEN="…" \
  -v "$PWD/var/owner:/data" \
  portfolio-hq-owner
```

The image reads `HOST` (default `0.0.0.0`), `PORT` (default `8080`),
`PORTFOLIO_HQ_OWNER_EXPORT` (default `/data/export.json`) and
`PORTFOLIO_HQ_OWNER_INBOX` (default `/data/inbox`). Mount a **persistent**
volume at `/data`: the chart inbox lives there, and an ephemeral filesystem
would discard received charts on restart.

### The exact remaining step, which needs the principal

Everything above is implemented and tested. What is **not** done, because it
cannot be done from inside this repository without provisioning and secrets:

1. **Choose the host.** Any provider that runs a container, terminates TLS, and
   offers a persistent volume. No provider is assumed, and none is provisioned
   here.
2. **Set `PORTFOLIO_HQ_OWNER_TOKEN` as a platform secret.** Not in a file, not
   in an image layer, not in this repository.
3. **Attach persistent storage** at `/data`.
4. **Confirm TLS termination** in front of the container, and that the host is
   not publicly listed. The service is private-by-token, not private-by-obscurity,
   but there is no reason to advertise it.
5. **Copy an export in** (or run the build step in the same deployment) and
   refresh it when accepted state changes.

No credential was collected, no infrastructure was purchased or provisioned, and
no hosted URL is claimed to exist.

## 8. What this interface still does not do

* No live account, brokerage connection or credential of any kind.
* No allocation check, order, or Stage-1 arming — **Stage 1 remains UNARMED and
  NOT EXECUTABLE**, untouched by this unit.
* No chart interpretation and no path from a chart to a recommendation.
* No staged account-entry/import flow: that belongs to the later final
  account-review stage, not here.
* No second allocator, and no portfolio figure computed in the browser.
