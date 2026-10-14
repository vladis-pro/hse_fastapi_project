import os
import platform
import psutil
import logging

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("host_monitor")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)

logger.addHandler(file_handler)
logger.info("Application started")

app_name = os.getenv("APP_NAME", "Infrastructure Host Monitor API")

app = FastAPI(title=app_name)


@app.get("/")
def root():
    return {"message": f"{app_name} is running"}


@app.get("/system")
def system_info():
    return {
        "hostname": platform.node(),
        "os": platform.system()
    }

@app.get("/cpu")
def cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)

    logger.info(f"CPU usage: {cpu_percent}%")

    return {
        "cpu_percent": cpu_percent
    }

@app.get("/memory")
def memory_info(unit: str = "gb"):

    if unit != "gb" and unit != "mb":
        logger.warning(f"Invalid memory unit: {unit}")

        raise HTTPException(
            status_code=400,
            detail="Unit must be 'gb' or 'mb'"
        )

    memory = psutil.virtual_memory()

    logger.info(f"Memory usage: {memory.percent}%")

    if unit == "mb":
        divisor = 1024 * 1024
    else:
        divisor = 1024 * 1024 * 1024

    return {
        "unit": unit,
        "total": round(memory.total / divisor, 2),
        "used": round(memory.used / divisor, 2),
        "available": round(memory.available / divisor, 2),
        "percent": memory.percent
    }

@app.get("/disk")
def disk_info():
    disk = psutil.disk_usage("/")

    logger.info(f"Disk usage: {disk.percent}%")

    return {
        "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
        "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
        "free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
        "percent": disk.percent
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "1.0.0"}

