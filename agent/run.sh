#!/usr/bin/env bash
# Run the agent

nohup /usr/bin/env python -u ./agent.py >agent.log 2>&1 &
