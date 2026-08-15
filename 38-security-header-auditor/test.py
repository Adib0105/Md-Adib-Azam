from app import audit

good = audit({
    "Content-Security-Policy": "default-src 'self'",
    "Strict-Transport-Security": "max-age=31536000",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=()",
})
assert good["score"] == 100
weak = audit({"Strict-Transport-Security": "max-age=60", "X-Content-Type-Options": "wrong"})
assert weak["score"] == 0
assert not weak["checks"]["strict-transport-security"]["passed"]
print("Security header auditor tests passed")
