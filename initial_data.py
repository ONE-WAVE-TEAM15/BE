import json
import logging
from sqlmodel import Session, select
from app.core.database import engine
from app.models.job import Job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        with open("dummy_data/job_dummy.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("dummy.json file not found.")
        return

    with Session(engine) as session:
        for item in data:
            # Handle both skills_need and skills_required from JSON
            # Pop both to avoid duplicate keyword argument error
            skills_required = item.pop("skills_need", None) or item.pop("skills_required", None)

            # Check for duplicates to prevent adding the same data multiple times
            existing_job = session.exec(
                select(Job).where(Job.company == item["company"], Job.title == item["title"])
            ).first()

            if not existing_job:
                job = Job(skills_required=skills_required, **item)
                session.add(job)
                logger.info(f"Adding job: {job.company} - {job.title}")
            else:
                logger.info(f"Job already exists: {item['company']} - {item['title']}")

        session.commit()
        logger.info("Data initialization completed.")

if __name__ == "__main__":
    init_db()
