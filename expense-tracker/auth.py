"""
Authentication utilities for JWT token management and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from config import settings
from database import getDb
from models import User
from schemas import TokenData

# Password hashing context
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2Scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


# ============================================================================
# Password Hashing
# ============================================================================

def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    """Verify a password against its hash."""
    return pwdContext.verify(plainPassword, hashedPassword)


def getPasswordHash(password: str) -> str:
    """Hash a password."""
    return pwdContext.hash(password)


# ============================================================================
# JWT Token Management
# ============================================================================

def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing token payload
        expiresDelta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    toEncode.update({"exp": expire, "type": "access"})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt


def createRefreshToken(data: dict) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        data: Dictionary containing token payload

    Returns:
        Encoded JWT refresh token string
    """
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    toEncode.update({"exp": expire, "type": "refresh"})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt


def verifyToken(
    token: str,
    credentialsException: HTTPException,
    expectedType: str = "access"
) -> TokenData:
    """
    Verify and decode a JWT token with type validation.

    Args:
        token: JWT token string
        credentialsException: Exception to raise if validation fails
        expectedType: Expected token type ('access' or 'refresh')

    Returns:
        TokenData object with user information

    Raises:
        credentialsException: If token is invalid or expired
        HTTPException: If token type doesn't match expected type
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        userId: int = payload.get("user_id")
        tokenType: str = payload.get("type")

        if username is None or userId is None:
            raise credentialsException

        # Verify token type matches expected type
        if tokenType != expectedType:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {expectedType}, got {tokenType}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(username=username, user_id=userId)

    except JWTError:
        raise credentialsException


# ============================================================================
# User Authentication
# ============================================================================

def authenticateUser(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.
    Uses constant-time operations to prevent timing attacks.

    Args:
        db: Database session
        username: User's username
        password: Plain text password

    Returns:
        User object if authentication successful, None otherwise
    """
    user = db.query(User).filter(User.username == username).first()

    # Always verify password even if user doesn't exist (constant time)
    # This prevents username enumeration through timing analysis
    dummyHash = getPasswordHash("dummy_password_for_timing_consistency")
    passwordHash = user.hashed_password if user else dummyHash

    passwordValid = verifyPassword(password, passwordHash)

    # Return user only if both user exists AND password is valid
    if not user or not passwordValid:
        return None

    return user


def getCurrentUser(
    token: str = Depends(oauth2Scheme),
    db: Session = Depends(getDb)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        token: JWT token from request header
        db: Database session

    Returns:
        Current User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    tokenData = verifyToken(token, credentialsException)

    user = db.query(User).filter(User.id == tokenData.user_id).first()
    if user is None:
        raise credentialsException

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )

    return user


def getCurrentActiveUser(
    currentUser: User = Depends(getCurrentUser)
) -> User:
    """
    Dependency to ensure user is active.

    Args:
        currentUser: Current user from getCurrentUser dependency

    Returns:
        Active User object

    Raises:
        HTTPException: If user account is inactive
    """
    if not currentUser.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return currentUser
