print("""The video corruptor
No outside library needed
How to use:
1.put this script to a folder
2.put a video into the same folder and you will be asked for a name
3.the result is record.mp4""")
import os, struct, re
from random import choice as r, randint as ri
from string import ascii_letters as _a
from shutil import copy

file_path = "record.mp4"
if os.path.exists(file_path):
    os.remove(file_path)

copy(input("choose file (with .mp4): "), "record.mp4")

def head(file_path):
    size_total = 0
    with open(file_path, "rb") as f:
        while data := f.read(8):
            size, name = struct.unpack(">I4s", data)
            if name == b"mdat":
                return size_total
            header_len = 8
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0]
                header_len = 16
            size_total += size
            f.seek(f.tell() + (size - header_len))
    return size_total

def foot(file_path):
    with open(file_path, "rb") as f:
        while data := f.read(8):
            size, name = struct.unpack(">I4s", data)
            real_size = struct.unpack(">Q", f.read(8))[0] if size == 1 else size
            if name == b"mdat":
                mdat_end = f.tell() - (16 if size == 1 else 8) + real_size
                return os.path.getsize(file_path) - mdat_end
            f.seek(f.tell() + (real_size - (16 if size == 1 else 8)))
    return 0
def rep(data_bytes, a, b):
    head_part = data_bytes[:a]
    slice_target = data_bytes[a:b]
    tail_part = data_bytes[b:]
    ab = (r(_a),r(_a))
    old_char = ab[0].encode('ascii')
    new_char = ab[1].encode('ascii')
    print(f"Replacing {ab[0]} with {ab[1]}")
    new_slice, count = re.subn(re.escape(old_char), new_char, slice_target)
    return head_part + new_slice + tail_part, count
    
def rep2(data_bytes, a, b,amount=1000):
    head = data_bytes[:a]
    s = bytearray(data_bytes[a:b]) 
    tail = data_bytes[b:]
    
    if len(s) > 0 and amount < len(s):
        for _ in range(amount):
            idx = ri(0, len(s) - 1)
            s[idx] = ord(r(_a))
    else:
        print("Something went wrong.")
    return head + bytes(s) + tail, amount 

# Execute
th = "record.mp4"

with open(th, "rb") as v:
    mp4_bytes = v.read()

h = head(th)
b_pos = len(mp4_bytes) - foot(th) 
if input("Choose type (1/any): ") == "1":
    new_mp4, count = rep(mp4_bytes, h, b_pos)
else:
    new_mp4, count = rep2(mp4_bytes, h, b_pos,int(input("Choose intensity(number default = 250): ") or "250"))

with open(th, "wb") as zz:
    zz.write(new_mp4)

print(f"Replaced {count} times")
