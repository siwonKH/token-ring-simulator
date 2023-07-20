import time
import threading
import queue
import tkinter as tk


class Node:
    def __init__(self, id, token=None):
        self.id = id
        self.next_node = None
        self.token = token
        self.data_queue = queue.Queue()
        self.button = None
        self.data_label = None  # 노드가 현재 가지고 있는 데이터를 표시할 라벨

    def set_next_node(self, node):
        self.next_node = node

    def pass_token_and_data(self):
        if self.token:
            data = None
            try:
                data = self.data_queue.get(block=False)
            except queue.Empty:
                pass

            if data:
                destination, message = data
                self.data_label.config(text=message)
                if self.id == destination:
                    print(f'노드 {self.id}번에 데이터 "{message}"가 도착했습니다.')
                    self.data_label.config(text=message + "\n 수신완료")
                else:
                    print(f'노드 {self.id}번이 데이터 "{message}"를 가지고 있습니다. 목적지는 노드 {destination}번 입니다.')
                    self.next_node.data_queue.put(data)

            else:
                print(f"노드 {self.id}번이 free 토큰을 가지고 있습니다")

            self.button.config(bg='green')  # 토큰이 있는 노드는 버튼 색을 초록색으로 변경
            time.sleep(3)  # 색상 변경을 볼 수 있도록 잠시 대기
            self.button.config(bg='SystemButtonFace')  # 현재 노드의 버튼 색을 기본색으로 변경

            self.data_label.config(text='Empty')

            self.next_node.token = self.token
            self.token = None


# 노드 생성
nodes = [Node(i) for i in range(5)]

# 링 구조로 노드 설정
for i in range(5):
    nodes[i].set_next_node(nodes[(i + 1) % 5])

# 노드 0이 처음에 토큰을 가지게 설정
nodes[0].token = 'TOKEN'


def add_input():
    start = entry.get()
    destination = entry2.get()
    message = entry3.get()
    entry.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)

    destination = int(destination)
    start = int(start)
    nodes[start].data_queue.put((destination, message))
    print(f"노드 {start}번에 데이터 '{message}'가 추가되었습니다. 목적지는 노드 {destination}입니다.")
    nodes[start].data_label.config(text=message)  # 새로운 데이터를 추가하면 바로 라벨을 업데이트


# GUI 생성
root = tk.Tk("LAN에서의 토큰 링 방식", "LAN에서의 토큰 링 방식", " LAN에서의 토큰 링 방식 시뮬레이션")
label = tk.Label(root, text="데이터를 전송하려면, [송신 노드 번호, 수신 노드 번호, 데이터] 순으로 입력하세요")
label.pack()

# 노드 버튼 및 데이터 라벨 생성
for node in nodes:
    node_frame = tk.Frame(root)
    node_frame.pack(side='left')

    node.button = tk.Button(node_frame, text=f"노드 {node.id}", state='disabled')
    node.button.pack()

    node.data_label = tk.Label(node_frame, text='Empty')
    node.data_label.pack()

entry = tk.Entry(root)
entry.pack()
entry2 = tk.Entry(root)
entry2.pack()
entry3 = tk.Entry(root)
entry3.pack()
button = tk.Button(root, text="전송", command=add_input)
button.pack()


def simulation():
    while True:
        for node in nodes:
            node.pass_token_and_data()


# 시뮬레이션 스레드 생성
threading.Thread(target=simulation).start()

# GUI 실행
root.mainloop()
