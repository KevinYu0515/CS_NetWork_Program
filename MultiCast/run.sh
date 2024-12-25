#!/bin/bash

# 啟動程式並儲存其 PID
echo "Running Sender_GUI.py..."
python3 Sender_GUI.py &
pids[0]=$!

sleep 1
echo "Running BR.py..."
python3 BR.py &
pids[1]=$!

sleep 1
echo "Running BC.py..."
python3 BC.py &
pids[2]=$!

sleep 1
echo "Running Receiver_GUI.py..."
python3 Receiver_GUI.py &
pids[3]=$!

echo "All scripts started. Press Ctrl+D to stop them."

# 等待使用者按下 Ctrl+D
while read -r; do :; done

# 停止所有程式
echo "Stopping all scripts..."
for pid in "${pids[@]}"; do
  kill "$pid" 2>/dev/null
done

echo "All scripts stopped."