from path import Path



def write_and_read():
    p = Path("./local_lib")
    if not p.exists(): return
    Path('local_lib/file_py').mkdir_p()
    with open('local_lib/file_py/file_py.txt', 'w') as f:
        f.write('Hello World')
    with open('local_lib/file_py/file_py.txt', 'r') as f:
        print(f.read())

if __name__ == '__main__':
    write_and_read()