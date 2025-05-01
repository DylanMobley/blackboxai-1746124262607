# middleware/roles.py

ROLES = {
    "admin": {
        "priority": 3,
        "permissions": [
            "manage_users",
            "view_metrics",
            "delete_content",
            "issue_tokens"
        ]
    },
    "user": {
        "priority": 2,
        "permissions": [
            "submit_requests",
            "view_own_data"
        ]
    },
    "guest": {
        "priority": 1,
        "permissions": [
            "view_public"
        ]
    }
}

def has_permission(role: str, permission: str) -> bool:
    """
    Check if a given role has a specific permission.
    """
    role_info = ROLES.get(role, {})
    return permission in role_info.get("permissions", [])
