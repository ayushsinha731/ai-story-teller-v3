"""Password hashing and verification utilities."""
import bcrypt


def hash_password(password: str) -> str:
    """Hash password using bcrypt.
    
    Note: bcrypt has a 72-byte limit, so we truncate the password.
    """
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = password.encode('utf-8')[:72]
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash.
    
    Note: Must truncate to match hashing behavior.
    """
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

