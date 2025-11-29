from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schemas.order_item import (
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemResponse,
)
from ..services.order_items import (
    create_order_item,
    get_order_item,
    list_order_items_by_order,
    update_order_item,
    delete_order_item,
)

router = APIRouter(prefix="/orders/{order_id}/items", tags=["order_items"])


class OrderItemsAPI:
    async def list(self, order_id: int, db: Session = Depends(get_db)) -> List[OrderItemResponse]:
        return list_order_items_by_order(db, order_id)

    async def get(self, order_id: int, item_id: int, db: Session = Depends(get_db)) -> OrderItemResponse:
        item = get_order_item(db, item_id)
        if not item or item.order_id != order_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item {item_id} not found in order {order_id}")
        return item

    async def create(self, order_id: int, payload: OrderItemCreate, db: Session = Depends(get_db)) -> OrderItemResponse:
        # Ensure order exists and is active
        order = (
            db.query(models.Order)
            .filter(models.Order.order_id == order_id, models.Order.is_active == True, models.Order.deleted_at.is_(None))
            .first()
        )
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found or inactive")
        try:
            return create_order_item(db, order_id, payload)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def update(self, order_id: int, item_id: int, payload: OrderItemUpdate, db: Session = Depends(get_db)) -> OrderItemResponse:
        # Ensure ownership
        exists = (
            db.query(models.OrderItem)
            .filter(models.OrderItem.order_item_id == item_id, models.OrderItem.order_id == order_id)
            .first()
        )
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item {item_id} not found in order {order_id}")
        try:
            updated = update_order_item(db, item_id, payload)
            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item {item_id} not found")
            return updated
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete(self, order_id: int, item_id: int, db: Session = Depends(get_db)) -> None:
        exists = (
            db.query(models.OrderItem)
            .filter(models.OrderItem.order_item_id == item_id, models.OrderItem.order_id == order_id)
            .first()
        )
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item {item_id} not found in order {order_id}")
        ok = delete_order_item(db, item_id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item {item_id} not found")


api = OrderItemsAPI()

# Routes
router.add_api_route("", api.list, methods=["GET"], response_model=List[OrderItemResponse])
router.add_api_route("/{item_id}", api.get, methods=["GET"], response_model=OrderItemResponse)
router.add_api_route("", api.create, methods=["POST"], response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
router.add_api_route("/{item_id}", api.update, methods=["PUT"], response_model=OrderItemResponse)
router.add_api_route("/{item_id}", api.delete, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
