"""Fail-closed authentication for the private owner interface.

Design rules this module exists to enforce:

* **No secret is ever committed.** The shared owner token comes from the
  process environment only. There is no default, no fallback, and no file in
  this repository that can supply one.
* **Missing configuration is not an open door.** ``require_owner_token``
  raises rather than returning a permissive value, and the service refuses to
  start when it raises — on every host, loopback included. A misconfigured
  deployment therefore serves nothing at all rather than serving private
  portfolio or chart data anonymously.
* **Sign-in alone is not authorization.** The session cookie is an HMAC over
  its own expiry, keyed by the owner token; rotating the token invalidates
  every outstanding session immediately, and a session cannot outlive its
  stated expiry.

Standard library only. Nothing here reads repository state or investment data.
"""

from __future__ import annotations

import hmac
import os
import time
from dataclasses import dataclass
from hashlib import sha256

#: Environment variable holding the shared owner secret. Set it as a platform
#: secret on the private host; never in a file, an image layer, or this repo.
TOKEN_ENV_VAR = "PORTFOLIO_HQ_OWNER_TOKEN"

#: Short secrets are the realistic failure mode for a hand-typed token, so the
#: floor is enforced at startup rather than trusted to the operator.
MIN_TOKEN_LENGTH = 32

SESSION_COOKIE_NAME = "phq_owner_session"
SESSION_TTL_SECONDS = 14 * 24 * 3600  # a fortnight — phone/tablet convenience
_SESSION_VERSION = "v1"

#: Login throttle: brute force against a >=32-character secret is already
#: impractical, but an unbounded login endpoint is still a free oracle and a
#: free CPU sink. Small, in-process, deliberately simple.
MAX_FAILED_ATTEMPTS = 8
LOCKOUT_SECONDS = 300


class OwnerAuthNotConfigured(RuntimeError):
    """No usable owner token in the environment. The caller must refuse to
    serve — never degrade to anonymous access."""


def require_owner_token(env: dict | None = None) -> str:
    """Return the configured owner token, or raise.

    Raising (rather than returning ``None``) is the point: there is no caller
    path that can accidentally treat "unconfigured" as "no auth needed".
    """
    source = os.environ if env is None else env
    token = (source.get(TOKEN_ENV_VAR) or "").strip()
    if not token:
        raise OwnerAuthNotConfigured(
            f"{TOKEN_ENV_VAR} is not set. The private owner interface refuses "
            "to start without it: an unauthenticated instance would expose "
            "private portfolio and chart information. Generate one with "
            "`python -c \"import secrets; print(secrets.token_urlsafe(32))\"` "
            "and set it as a secret on the host."
        )
    if len(token) < MIN_TOKEN_LENGTH:
        raise OwnerAuthNotConfigured(
            f"{TOKEN_ENV_VAR} is only {len(token)} characters; at least "
            f"{MIN_TOKEN_LENGTH} are required."
        )
    return token


def token_matches(supplied: object, token: str) -> bool:
    """Constant-time comparison of a submitted secret against the owner token."""
    if not isinstance(supplied, str) or not supplied:
        return False
    return hmac.compare_digest(supplied.encode("utf-8"), token.encode("utf-8"))


# ── stateless sessions ───────────────────────────────────────────────────────

@dataclass(frozen=True)
class SessionSigner:
    """Issues and verifies opaque, self-expiring session values.

    A session value is ``"<expiry-epoch>.<hex-hmac>"``. The HMAC covers the
    version and the expiry, keyed by the owner token, so a client can neither
    forge a value nor extend one it already holds. No server-side session
    store is needed, which keeps the hosted component stateless apart from the
    chart inbox itself.
    """

    token: str

    def _signature(self, expires_at: int) -> str:
        message = f"{_SESSION_VERSION}|{expires_at}".encode("utf-8")
        return hmac.new(self.token.encode("utf-8"), message, sha256).hexdigest()

    def issue(self, *, now: float | None = None,
              ttl_seconds: int = SESSION_TTL_SECONDS) -> str:
        expires_at = int((time.time() if now is None else now)) + int(ttl_seconds)
        return f"{expires_at}.{self._signature(expires_at)}"

    def verify(self, value: object, *, now: float | None = None) -> bool:
        if not isinstance(value, str) or value.count(".") != 1:
            return False
        raw_expiry, signature = value.split(".", 1)
        try:
            expires_at = int(raw_expiry)
        except ValueError:
            return False
        # Verify the signature before honouring the expiry so an attacker
        # cannot learn anything from ordering, and reject expired values even
        # when correctly signed.
        expected = self._signature(expires_at)
        if not hmac.compare_digest(signature, expected):
            return False
        return expires_at > (time.time() if now is None else now)


# ── login throttle ───────────────────────────────────────────────────────────

class LoginThrottle:
    """Bounded failed-attempt counter with a fixed lockout window.

    Keyed by caller-chosen identity (the remote address). Deliberately
    in-process and non-persistent: it is a speed bump on a single instance,
    not a distributed rate limiter, and it is documented as such.
    """

    def __init__(self, *, max_attempts: int = MAX_FAILED_ATTEMPTS,
                 lockout_seconds: int = LOCKOUT_SECONDS,
                 max_tracked: int = 2048) -> None:
        self.max_attempts = int(max_attempts)
        self.lockout_seconds = int(lockout_seconds)
        self.max_tracked = int(max_tracked)
        self._failures: dict[str, tuple[int, float]] = {}

    def _prune(self, now: float) -> None:
        if len(self._failures) <= self.max_tracked:
            return
        # Drop entries whose lockout window has already elapsed; if that is not
        # enough, drop oldest-first. Bounded memory under hostile traffic.
        self._failures = {
            key: value for key, value in self._failures.items()
            if now - value[1] < self.lockout_seconds
        }
        if len(self._failures) > self.max_tracked:
            ordered = sorted(self._failures.items(), key=lambda kv: kv[1][1])
            self._failures = dict(ordered[-self.max_tracked:])

    def locked_out(self, identity: str, *, now: float | None = None) -> bool:
        moment = time.time() if now is None else now
        entry = self._failures.get(identity)
        if entry is None:
            return False
        count, last_failure = entry
        if moment - last_failure >= self.lockout_seconds:
            self._failures.pop(identity, None)
            return False
        return count >= self.max_attempts

    def record_failure(self, identity: str, *, now: float | None = None) -> None:
        moment = time.time() if now is None else now
        count, last_failure = self._failures.get(identity, (0, moment))
        if moment - last_failure >= self.lockout_seconds:
            count = 0
        self._failures[identity] = (count + 1, moment)
        self._prune(moment)

    def record_success(self, identity: str) -> None:
        self._failures.pop(identity, None)
