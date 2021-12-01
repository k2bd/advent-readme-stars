FROM python:3.9

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN pip install "poetry==1.1.11"

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

COPY . .
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "-m", "advent_readme_stars"]
