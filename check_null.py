with open('classes/Menu.py', 'rb') as f:
    content = f.read()
    if b'\x00' in content:
        null_positions = [i for i, byte in enumerate(content) if byte == 0]
        print(f"发现{len(null_positions)}个空字节在以下位置：{null_positions}")
    else:
        print("文件干净，没有空字节") 