#!/bin/bash
printf "entrypoint started /n"
uvicorn main:app --reload --host 0.0.0.0 --port 7000