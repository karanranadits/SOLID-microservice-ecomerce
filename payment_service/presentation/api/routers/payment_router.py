from fastapi import APIRouter, Depends, HTTPException, Header
from application.dtos.requests import ProcessPaymentRequestDTO
from application.dtos.responses import ProcessPaymentResponseDTO
from application.use_cases.process_payment import ProcessPaymentUseCase
from presentation.api.dependencies import get_process_payment_use_case, verify_token

router = APIRouter()

@router.post("/pay", response_model=ProcessPaymentResponseDTO)
def process_payment(
    request: ProcessPaymentRequestDTO, 
    use_case: ProcessPaymentUseCase = Depends(get_process_payment_use_case),
    username: str = Depends(verify_token)
):
    try:
        payment = use_case.execute(
            username=username,
            order_id=request.order_id, 
            amount=request.amount
        )
        
        # Map Entity to Response DTO
        return ProcessPaymentResponseDTO(
            status=payment.status,
            transaction_id=payment.transaction_id,
            user=username,
            checkout_url=payment.checkout_url
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
