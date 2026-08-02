import logging
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "memory" / "app.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("nyvexa")
