import mysocket

# for i in range(5):
#     client = mysocket.mysocket()
#     client.connect(('127.0.0.1', 12000))
#     for i in range(5):
#         data = bytes(str(i), encoding='utf-8')
#         client.send(data)
#     client.close()

client = mysocket.mysocket()
client.connect(('127.0.0.1', 12000))
for i in range(5):
    data = bytes(str(i), encoding='utf-8')
    client.send(data)
client.close()