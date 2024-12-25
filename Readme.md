依照 113 學年度上學期的課程 Lab 安排順序

內容主要使用的 python 套件
- 網路：socket、threading、struct
- GUI：tkinter/customtkinter

## RPC

說明：此 Lab 展現使用 RPC 方式建立一個簡易論壇
- 問題點：多個 Client 的同步問題，但本次設計不探討如何解決

執行 server 和 client 即可，預設使用 localhost:8810
- `python RPC/server/main.py`
- `python RPC/client/main.py`

## TCP

說明：此 Lab 展現使用 TCP 連線傳遞數字，並於 Client、Server 之間各作減一之後傳送，最後數字為 0 時斷開連線
- 只能輸入一次數字
- Server 斷開，Client 就無法連回去

執行 server 和 client 即可，預設使用 localhost:8888
- `python TCP/server.py`
- `python TCP/client_GUI.py [server IP]`

## pop3

說明：此 Lab 藉由 pop3 實現收信功能， 另外寫了 smtp.py 實現發信功能
- 這邊僅提供 client 程式碼，所以缺少 mail server，無法連線是正常的

## UDP

說明：此 Lab 展現使用 UDP 連線傳遞數字，並於 Client、Server 之間各作減一之後傳送，最後數字為 0 時停止傳送
- 只能輸入一次數字
- Server 關閉，Client 會有超時機制等待 Server 傳送，因此當 Server 恢復時，Client 就會自動恢復接收、傳送 

執行 server 和 client 即可，預設使用 localhost:8888
- `python UDP/server.py`
- `python UDP/client_GUI.py [server IP]`

## SAWSocket

說明：此 Lab 展現使用 SlideWindow 來優化 UDP 接收，當有封包丟失時，則從該丟失的封包重新開始發送 n 個封包（n 為 window size）。
- Server 藉由隨機丟失封包的方式控制 ack 的變化，來模擬 UDP 丟失封包，Client 須重送的情況
- 如果 Client、Server 超時沒有接收到 ack 或 data，同樣也會重送

執行 server 和 client 即可，預設使用 localhost:8888，窗口大小為 4
- `python SAW/SAWClient.py [server IP:PORT] [window size]`
- `python SAW/SAWServer.py [window size]`

> 注意：client 和 server 的 window size 要一樣

## SecureSocket

說明：使用 openssl 提供的 ssl 加密傳輸資料，情境同樣為 Client、Server 數字間減一後傳送，直到 0 為止

1. 在 SecureSocket 資料夾底下使用 openssl 生成 key 和 certificate
`openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.cer -config ssl.conf`

2. 由於要抓取 key、certificate 的相對路徑，所以執行程式需要先切換至 SecureSocket 資料夾內，預設使用 localhost:8888
- `cd SecureSocket`
- `python server.py`
- `python client_GUI.py [server IP]`

## Unblock

說明：此 Lab 展現的是 Consumer/Producer，Server 提供兩個 port 擔任 Consumer 和 Producer 的角色，Client 可以選擇成為 Producer 向 queue 提供 data，或成為 Consumer 從 queue 取出資料
- Consumer 有作超時機制等待 queue 內出現 new data
- 當多個 Consumer 等待時，將採用隨機分配 new data 給任一個等待的 Consumer

執行 server 和 client 即可，預設使用 localhost:8881 作為 Consumer，localhost:8880 作為 Producer
- `python Unblock/client_GUI.py`
- `python Unblock/server.py`

## MultiCast

說明：此 Lab 展現的是群組廣播，Sender 於 225.3.2.1 群組，Receiver 於 225.6.7.8 群組，群組間經由 BR、BC 建立 TCP 傳遞訊息
- BC 必須等待 BR 建立，才能成功建立 TCP 連線
- 只有作單向傳遞，也就是說 Sender 沒辦法確認 Receiver 有沒有接收到

使用 shell 依序執行程式（BC、BR 使用 TCP 連線，所以有先後執行的連線關係），按下 Ctrl+D 中止執行
Sender：預設使用 localhost:6666
Receiver：預設使用 localhost:8888
BR：TCP 預設使用 7777 port，MultCast 預設使用 6666 port
BC：TCP 預設使用 7777 port，MultCast 預設使用 8888 port
- `source MultiCast/run.sh`