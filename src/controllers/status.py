from fastapi import APIRouter, status

from src.utils.responses import APIResponse

status_router = APIRouter(
    prefix="/status",
    tags=["Status"],
)


@status_router.get(
    "",
    response_class=APIResponse,
    response_description="Status check",
    responses={
        status.HTTP_200_OK: {"description": "Status check successful"},
        status.HTTP_404_NOT_FOUND: {"description": "Status check failed"},
    },
)
async def status_check() -> APIResponse:
    return APIResponse(
        message="Status check successful",
        status_code=status.HTTP_200_OK,
    )
