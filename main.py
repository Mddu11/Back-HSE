import asyncio
import time
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Async Squares Demo")



class CalculateRequest(BaseModel):
    numbers: List[int] = Field(..., example=[5, 3, 10])
    delays: List[float] = Field(..., example=[1, 2, 0.5])


class CalculationResult(BaseModel):
    number: int
    square: int
    delay: float
    time: float


class CalculateResponse(BaseModel):
    results: List[CalculationResult]
    total_time: float
    parallel_faster_than_sequential: bool




async def calculate_square(number: int, delay: float) -> CalculationResult:
    start = time.perf_counter()
    await asyncio.sleep(delay)
    square = number ** 2
    elapsed = time.perf_counter() - start

    return CalculationResult(
        number=number,
        square=square,
        delay=delay,
        time=round(elapsed, 2)
    )



@app.post("/calculate/", response_model=CalculateResponse)
async def calculate(request: CalculateRequest):
    start_total = time.perf_counter()

    tasks = [
        calculate_square(n, d)
        for n, d in zip(request.numbers, request.delays)
    ]

    results = await asyncio.gather(*tasks)

    total_time = round(time.perf_counter() - start_total, 2)
    sequential_time = sum(request.delays)

    return CalculateResponse(
        results=results,
        total_time=total_time,
        parallel_faster_than_sequential=total_time < sequential_time
    )
