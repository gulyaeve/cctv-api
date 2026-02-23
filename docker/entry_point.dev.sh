#!/bin/sh

alembic upgrade head

uvicorn app.main:app
