"""Router pour l'authentification."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas import LoginPayload, UserResponse
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, verify_password
from app.core.storage import add_audit_log, get_user_by_email, seed_default_users
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)) -> dict:
    # Ensure default users exist
    seed_default_users(db)

    user = get_user_by_email(db, payload.email)

    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    add_audit_log(db, "login", user.email, f"Connexion réussie pour {user.email}")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
