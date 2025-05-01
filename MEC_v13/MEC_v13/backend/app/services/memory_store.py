import threading
import time
import json
from sqlalchemy.orm import Session
from backend.models import Persona, User  # Assuming SQLAlchemy models for User and Persona

# In-memory storage
_memory = {}
_expiry = {}
_lock = threading.Lock()

def _is_expired(key: str) -> bool:
    """ Internal check to see if a key has expired. """
    if key not in _expiry:
        return False
    return time.monotonic() > _expiry[key]

def set_memory(key: str, value, ttl: float = None, db: Session = None, user_id: str = None) -> None:
    """ Store a value in memory with an optional TTL (Time-to-Live). Optionally sync with DB. """
    with _lock:
        # Set in-memory value
        _memory[key] = value
        if ttl:
            _expiry[key] = time.monotonic() + ttl
        
        # Sync with the database if necessary (e.g., storing user persona)
        if db and user_id:
            sync_to_db(user_id, key, value, db)

def get_memory(key: str, db: Session = None, user_id: str = None):
    """ Retrieve a memory value if it exists and is not expired. Fallback to DB if not in memory. """
    with _lock:
        if _is_expired(key):
            del _memory[key]
            del _expiry[key]
            return None
        
        # Return from memory if available
        if key in _memory:
            return _memory[key]
        
        # Fallback to DB if not in memory
        if db and user_id:
            return load_from_db(user_id, key, db)
        
        return _memory.get(key)

def delete_memory(key: str) -> None:
    """ Remove a key from memory and TTL table. """
    with _lock:
        _memory.pop(key, None)
        _expiry.pop(key, None)

def reset_memory() -> None:
    """ Clear all memory and TTL records. """
    with _lock:
        _memory.clear()
        _expiry.clear()

def list_memory() -> dict:
    """ Return all non-expired memory entries. """
    now = time.monotonic()
    with _lock:
        return {
            k: v for k, v in _memory.items()
            if k not in _expiry or _expiry[k] > now
        }

def snapshot_memory(path: str = "memory_snapshot.json") -> None:
    """ Export current non-expired memory to a JSON file. """
    with _lock:
        data = {
            "memory": list_memory(),
            "timestamp": time.time()
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def load_snapshot(path: str = "memory_snapshot.json") -> None:
    """ Load memory state from a snapshot file. TTLs are not preserved. """
    with open(path, "r") as f:
        data = json.load(f)
    with _lock:
        for key, val in data.get("memory", {}).items():
            _memory[key] = val

# Database Sync Functions
def sync_to_db(user_id: str, key: str, value: any, db: Session) -> None:
    """
    Sync the in-memory data to the database for long-term persistence.
    """
    if key == "user_persona":  # Example for syncing persona data
        persona_data = value  # Assume value is the persona data dictionary
        persona = db.query(Persona).filter(Persona.user_id == user_id).first()
        
        if persona:
            # Update existing persona
            persona.persona_name = persona_data["persona"]
            persona.tone = persona_data["tone"]
            persona.energy_level = persona_data["energy_level"]
            persona.goal = persona_data["goal"]
            persona.updated_at = time.time()
        else:
            # Create new persona if not found
            new_persona = Persona(
                user_id=user_id,
                persona_name=persona_data["persona"],
                tone=persona_data["tone"],
                energy_level=persona_data["energy_level"],
                goal=persona_data["goal"],
                updated_at=time.time()
            )
            db.add(new_persona)

        db.commit()

def load_from_db(user_id: str, key: str, db: Session) -> any:
    """
    Load data from the database for a given key (e.g., user persona, emotional state).
    """
    if key == "user_persona":
        persona = db.query(Persona).filter(Persona.user_id == user_id).first()
        if persona:
            return {
                "persona": persona.persona_name,
                "tone": persona.tone,
                "energy_level": persona.energy_level,
                "goal": persona.goal
            }
    return None
