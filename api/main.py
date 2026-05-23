from fastapi import FastAPI
from dotenv import load_dotenv
from routers.journal_router import router as journal_router
import logging

# Load our environment flags securely
load_dotenv()

# 1 & 2 & 3. Configure logging infrastructure at the INFO threshold
logging.basicConfig(
    level=logging.INFO,
    # This format adds an accurate timestamp, the severity level, and the message
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    # Directs our structured logs directly to the standard output console stream
    handlers=[logging.StreamHandler()]
)

# Initialize our named logging recorder for this specific file module
logger = logging.getLogger("main")

# Create the primary FastAPI application configuration core block
app = FastAPI(
    title="LearningSteps API", 
    description="A simple learning journal API for tracking daily work, struggles, and intentions"
)

# 4. Test by adding a structured log message when the application boots up cleanly
logger.info("Security tracking infrastructure successfully initialized. LearningSteps API is online.")

# Mount our verified front counter router endpoints
app.include_router(journal_router)