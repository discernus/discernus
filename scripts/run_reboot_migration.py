import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

def main():
    """
    Runs the alembic migration for the reboot schema.
    This script ensures that the .env file is loaded before alembic runs,
    guaranteeing that the database URL is available.
    """
    # Load environment variables from .env file
    # load_dotenv() will automatically find .env in current or parent directories
    load_dotenv()

    # Verify the database URL is loaded
    db_url = os.getenv("REBOOT_DATABASE_URL")
    if not db_url:
        print("Error: REBOOT_DATABASE_URL not found in environment variables.")
        print("Please ensure your .env file contains: REBOOT_DATABASE_URL=postgresql://...")
        return

    print(f"Using database: {db_url}")

    # Create an AlembicConfig object
    # We assume this script is run from the project root
    alembic_cfg = Config("src/reboot/alembic.ini")

    # Generate the revision
    print("Generating migration...")
    try:
        command.revision(alembic_cfg, autogenerate=True, message="Create initial reboot jobs and results tables")
        print("Migration generated successfully.")
    except Exception as e:
        print(f"Error generating migration: {e}")
        return

    # Apply the migration
    print("Applying migration...")
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migration applied successfully.")
    except Exception as e:
        print(f"Error applying migration: {e}")
        return

    print("Database setup complete!")

if __name__ == "__main__":
    main() 