FROM python:3.9

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

COPY src .
COPY pyproject.toml .

RUN pip install -e .

CMD ["python", "-m", "advent_readme_stars"]