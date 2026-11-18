"""Customer Accounts microservice security configuration."""

from flask_talisman import Talisman


def configure_security(app):
    """Apply the application's browser security headers."""
    Talisman(
        app,
        force_https=not app.config.get("TESTING", False),
        content_security_policy={
            "default-src": ["'self'"],
            "object-src": ["'none'"],
            "frame-ancestors": ["'none'"],
        },
    )
