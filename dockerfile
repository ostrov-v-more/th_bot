# 1. Base image
FROM python:3.12

# 2. Set environment variables
# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# 3. Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# 4. Set work directory
WORKDIR /app

# 5. Copy only dependency files first (for better Docker caching)
COPY pyproject.toml poetry.lock ./

# 6. Install dependencies
# --no-root skips installing the current project as a package
RUN poetry install --no-root --only main

# 7. Copy the rest of the code
COPY . .

# 8. Start the bot
CMD ["python", "main.py"]