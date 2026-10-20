from app.bot.handlers.commands import router as commands_router
from app.bot.handlers.tournaments import router as tournaments_router
from app.bot.handlers.admin import router as admin_router

router = commands_router
router.include_router(tournaments_router)
router.include_router(admin_router)

__all__ = ["router"]
