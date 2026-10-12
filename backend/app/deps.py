"""Shared FastAPI dependencies (e.g. Redis client).

Wire Redis here when you implement the shortlink service.
"""

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]
