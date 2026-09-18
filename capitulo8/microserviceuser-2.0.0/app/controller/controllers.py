from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from controller.dtos import (
    UserCreateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from dependencies.dependencies import get_user_service
from entities.business import User
from services.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario",
)
def insert(
    request: UserCreateDTO,
    service: UserService = Depends(get_user_service),
) -> UserResponseDTO:
    user = User(
        name=request.name,
        email=str(request.email),
        address=request.address,
    )

    try:
        service.insert(user)

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            address=user.address,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[UserResponseDTO],
    summary="Listar todos los usuarios",
)
def list_all(
    service: UserService = Depends(get_user_service),
) -> list[UserResponseDTO]:
    users = service.list_all()

    return [
        UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            address=user.address,
        )
        for user in users
    ]


@router.put(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Actualizar un usuario",
)
def update(
    user_id: int,
    request: UserUpdateDTO,
    service: UserService = Depends(get_user_service),
) -> UserResponseDTO:
    user = User(
        id=user_id,
        name=request.name,
        email=str(request.email),
        address=request.address,
    )

    try:
        service.update(user)

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            address=user.address,
        )

    except ValueError as error:
        message = str(error)

        status_code = (
            status.HTTP_404_NOT_FOUND
            if message == "Usuario no encontrado"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=status_code,
            detail=message,
        ) from error


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
)
def delete(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> Response:
    try:
        service.delete(user_id)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error